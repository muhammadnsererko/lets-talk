"""
Routes for handling OTP (One-Time Password) related API endpoints.
Includes endpoint for sending OTP via synthesized speech.
"""
from flask import Blueprint, request, jsonify
from utils.otp import generate_otp
from services.polly_service import synthesize_speech
import os
import json

BACKUP_CODES_FILE = os.path.join(os.path.dirname(__file__), '..', 'backup_codes.json')

otp_bp = Blueprint('otp', __name__)

def load_backup_codes():
    if os.path.exists(BACKUP_CODES_FILE):
        with open(BACKUP_CODES_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_backup_codes(codes):
    with open(BACKUP_CODES_FILE, 'w') as f:
        json.dump(codes, f)

def generate_backup_codes(n=5):
    return [str(generate_otp()) for _ in range(n)]

@otp_bp.route('/calls/otp', methods=['POST'])
def send_otp():
    """
    Handle POST requests to /calls/otp to generate and send an OTP to a user.
    Expects JSON with 'user_id'.
    Returns a simulated audio response and OTP details (for testing).
    """
    data = request.get_json()
    user_id = data.get('user_id')

    if not user_id:
        return jsonify({"error": "user_id required"}), 400

    otp = generate_otp()
    otp_text = f"Your O T P is {otp}. Please enter it now."

    audio_response = synthesize_speech(otp_text)
    if "error" in audio_response:
        return jsonify({"error": audio_response["error"]}), 500

    print(f"Simulating sending OTP {otp} to user {user_id}")

    return jsonify({
        "status": "otp_sent",
        "otp_id": f"otp_{user_id}_{otp}",
        "otp": otp  # Remove this in production
    })

@otp_bp.route('/calls/otp/verify', methods=['POST'])
def verify_otp():
    """
    Placeholder endpoint for verifying an OTP submitted by the user.
    Expects JSON with 'user_id' and 'otp'.
    Returns a simulated verification response.
    """
    data = request.get_json()
    user_id = data.get('user_id')
    otp = data.get('otp')
    # Placeholder logic for OTP verification
    return jsonify({"status": "verification_placeholder", "user_id": user_id, "otp": otp})

@otp_bp.route('/calls/otp/replay', methods=['POST'])
def replay_otp_voice():
    """
    Placeholder endpoint for replaying the OTP voice message to the user.
    Expects JSON with 'user_id'.
    Returns a simulated audio response.
    """
    data = request.get_json()
    user_id = data.get('user_id')
    # Placeholder logic for replaying OTP voice
    return jsonify({"status": "replay_placeholder", "user_id": user_id})

@otp_bp.route('/calls/otp/enroll', methods=['POST'])
def enroll_user():
    data = request.get_json()
    user_id = data.get('user_id', 'user001')  # Use 'user001' as default if not provided
    backup_codes = load_backup_codes()
    if user_id not in backup_codes:
        codes = generate_backup_codes()
        backup_codes[user_id] = codes
        save_backup_codes(backup_codes)
    else:
        codes = backup_codes[user_id]
    return jsonify({"user_id": user_id, "backup_codes": codes})
    if not user_id:
        return jsonify({"error": "user_id required"}), 400
    codes = load_backup_codes()
    if user_id in codes:
        return jsonify({"backup_codes": codes[user_id], "status": "already_enrolled"})
    backup_codes = generate_backup_codes()
    codes[user_id] = backup_codes
    save_backup_codes(codes)
    return jsonify({"backup_codes": backup_codes, "status": "enrolled"})