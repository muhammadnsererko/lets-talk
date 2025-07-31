import json
import os
import secrets
import datetime
import pyttsx3
import hashlib
import logging
from config import Config

logger = logging.getLogger(__name__)
OTP_STORE_FILE = Config.OTP_STORE_FILE
OTP_EXPIRY_MINUTES = Config.OTP_EXPIRY_MINUTES


def generate_otp():
    """
    Generate a cryptographically secure random 6-digit OTP (One-Time Password).
    Returns:
        str: A 6-digit OTP.
    """
    return str(secrets.randbelow(900000) + 100000)

def store_otp(user_id, otp):
    """
    Stores the OTP for a user with a 5-minute expiration.
    """
    try:
        if not os.path.exists(OTP_STORE_FILE):
            with open(OTP_STORE_FILE, 'w') as f:
                json.dump({}, f)

        with open(OTP_STORE_FILE, 'r+') as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = {}
            
            expiration_time = datetime.datetime.now() + datetime.timedelta(minutes=OTP_EXPIRY_MINUTES)
            hashed_otp = hashlib.sha256(otp.encode()).hexdigest()
            
            data[user_id] = {
                "otp": hashed_otp,
                "expires_at": expiration_time.isoformat()
            }
            
            f.seek(0)
            json.dump(data, f, indent=2)
            f.truncate()
            return user_id
    except (IOError, OSError) as e:
        from voice_api.utils.custom_exceptions import OTPStorageError
        raise OTPStorageError(f"Failed to store OTP: {str(e)}")

def get_stored_otp(user_id, otp):
    """
    Verify the OTP for a user against the stored hash.
    """
    if not os.path.exists(OTP_STORE_FILE):
        return None

    with open(OTP_STORE_FILE, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            return None
    
    if user_id not in data:
        return None
    
    stored_data = data[user_id]
    expires_at = datetime.datetime.fromisoformat(stored_data['expires_at'])
    
    if datetime.datetime.now() >= expires_at:
        return None
    
    hashed_input = hashlib.sha256(otp.encode()).hexdigest()
    if hashed_input == stored_data['otp']:
        return otp
    
    return None

def speak_otp(otp):
    """
    Speaks the OTP aloud using configurable settings.
    """
    try:
        engine = pyttsx3.init()
        
        # Set properties from configuration
        engine.setProperty('rate', Config.DEFAULT_VOICE_RATE)
        engine.setProperty('volume', Config.DEFAULT_VOICE_VOLUME)
        
        # Log voice output
        logger.info(f"Speaking OTP for user")
        
        engine.say(f"Your one time password is {', '.join(list(otp))}")
        engine.runAndWait()
    except Exception as e:
        logger.error(f"Error speaking OTP: {str(e)}")
        # Fallback to print if TTS fails
        print(f"[TTS Fallback] Your OTP is: {', '.join(list(otp))}")