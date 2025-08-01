"""
OTP (One-Time Password) Blueprint
Handles voice-based 2FA authentication via pyttsx3
"""
import os
import json
import uuid
from datetime import datetime, timedelta
from flask import Blueprint, request, jsonify, current_app
import pyttsx3

otp_bp = Blueprint('otp', __name__, url_prefix='/calls')

# OTP storage configuration
OTP_STORE_FILE = os.path.join('data', 'otps.json')
VOICE_SETTINGS_FILE = os.path.join('data', 'voice_settings.json')

# Ensure data directory exists
os.makedirs('data', exist_ok=True)

def get_voice_engine():
    """Initialize and return TTS engine"""
    try:
        engine = pyttsx3.init()
        
        # Load voice settings if they exist
        if os.path.exists(VOICE_SETTINGS_FILE):
            with open(VOICE_SETTINGS_FILE, 'r') as f:
                settings = json.load(f)
                engine.setProperty('rate', settings.get('rate', 150))
                engine.setProperty('volume', settings.get('volume', 0.9))
        else:
            # Default settings
            engine.setProperty('rate', 150)
            engine.setProperty('volume', 0.9)
        
        return engine
    except Exception as e:
        current_app.logger.error(f"Failed to initialize TTS engine: {e}")
        return None

def load_otps():
    """Load OTPs from storage"""
    if not os.path.exists(OTP_STORE_FILE):
        return {}
    
    try:
        with open(OTP_STORE_FILE, 'r') as f:
            return json.load(f)
    except Exception:
        return {}

def save_otps(otps):
    """Save OTPs to storage"""
    with open(OTP_STORE_FILE, 'w') as f:
        json.dump(otps, f, indent=2)

def generate_otp(length=6):
    """Generate a random OTP"""
    import secrets
    return ''.join([str(secrets.randbelow(10)) for _ in range(length)])

def speak_otp(phone_number, otp):
    """Speak OTP using TTS"""
    engine = get_voice_engine()
    if not engine:
        return False
    
    try:
        message = f"Hello. Your verification code is {otp}. Repeat, your code is {otp}."
        engine.say(message)
        engine.runAndWait()
        return True
    except Exception as e:
        current_app.logger.error(f"Failed to speak OTP: {e}")
        return False

@otp_bp.route('/otp', methods=['POST'])
def initiate_otp():
    """Initiate OTP generation and voice call"""
    data = request.get_json()
    
    if not data or 'phone_number' not in data:
        return jsonify({'error': 'Phone number is required'}), 400
    
    phone_number = data['phone_number']
    user_id = data.get('user_id', 'default_user')
    
    # Generate OTP
    otp = generate_otp()
    
    # Store OTP with expiration
    otps = load_otps()
    otps[phone_number] = {
        'otp': otp,
        'user_id': user_id,
        'created_at': datetime.now().isoformat(),
        'expires_at': (datetime.now() + timedelta(minutes=5)).isoformat(),
        'attempts': 0,
        'verified': False
    }
    save_otps(otps)
    
    # Speak OTP via TTS
    success = speak_otp(phone_number, otp)
    
    if success:
        return jsonify({
            'message': 'OTP sent via voice call',
            'session_id': str(uuid.uuid4()),
            'expires_in': 300
        }), 200
    else:
        return jsonify({'error': 'Failed to send OTP via voice'}), 500

@otp_bp.route('/otp/verify', methods=['POST'])
def verify_otp():
    """Verify OTP code"""
    data = request.get_json()
    
    if not data or 'phone_number' not in data or 'otp' not in data:
        return jsonify({'error': 'Phone number and OTP are required'}), 400
    
    phone_number = data['phone_number']
    provided_otp = data['otp']
    
    otps = load_otps()
    
    if phone_number not in otps:
        return jsonify({'error': 'No OTP found for this phone number'}), 404
    
    otp_data = otps[phone_number]
    
    # Check if OTP has expired
    expires_at = datetime.fromisoformat(otp_data['expires_at'])
    if datetime.now() > expires_at:
        del otps[phone_number]
        save_otps(otps)
        return jsonify({'error': 'OTP has expired'}), 400
    
    # Check if already verified
    if otp_data.get('verified', False):
        return jsonify({'error': 'OTP already used'}), 400
    
    # Check attempts
    if otp_data['attempts'] >= 3:
        del otps[phone_number]
        save_otps(otps)
        return jsonify({'error': 'Maximum attempts exceeded'}), 400
    
    # Verify OTP
    if provided_otp == otp_data['otp']:
        otp_data['verified'] = True
        otp_data['verified_at'] = datetime.now().isoformat()
        save_otps(otps)
        
        return jsonify({
            'message': 'OTP verified successfully',
            'user_id': otp_data['user_id']
        }), 200
    else:
        otp_data['attempts'] += 1
        save_otps(otps)
        return jsonify({'error': 'Invalid OTP'}), 400

@otp_bp.route('/otp/status/<phone_number>', methods=['GET'])
def get_otp_status(phone_number):
    """Get OTP status for a phone number"""
    otps = load_otps()
    
    if phone_number not in otps:
        return jsonify({'error': 'No OTP found'}), 404
    
    otp_data = otps[phone_number]
    expires_at = datetime.fromisoformat(otp_data['expires_at'])
    is_expired = datetime.now() > expires_at
    
    return jsonify({
        'phone_number': phone_number,
        'created_at': otp_data['created_at'],
        'expires_at': otp_data['expires_at'],
        'is_expired': is_expired,
        'verified': otp_data.get('verified', False),
        'attempts': otp_data['attempts']
    }), 200