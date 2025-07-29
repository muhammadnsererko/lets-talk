import json
import os
import secrets
import datetime
import pyttsx3
from config import Config

OTP_STORE_FILE = Config.OTP_STORE_FILE


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
    if not os.path.exists(OTP_STORE_FILE):
        with open(OTP_STORE_FILE, 'w') as f:
            json.dump({}, f)

    with open(OTP_STORE_FILE, 'r+') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            data = {}
        
        expiration_time = datetime.datetime.now() + datetime.timedelta(minutes=5)
        otp_id = f"otp_{user_id}_{otp}"
        
        data[otp_id] = {
            "user_id": user_id,
            "otp": otp,
            "expires_at": expiration_time.isoformat()
        }
        
        f.seek(0)
        json.dump(data, f, indent=2)
        f.truncate()
        return otp_id

def speak_otp(otp):
    """
    Speaks the OTP aloud.
    """
    engine = pyttsx3.init()
    
    # Set properties
    engine.setProperty('rate', 150)
    engine.setProperty('volume', 1.0)

    # Log voice output
    print(f"Speaking OTP: {', '.join(list(otp))}")

    engine.say(f"Your one time password is {', '.join(list(otp))}")
    engine.runAndWait()

def get_stored_otp(user_id):
    """
    Retrieves the latest valid OTP for a user.
    Returns:
        str: The OTP if found and not expired, None otherwise.
    """
    if not os.path.exists(OTP_STORE_FILE):
        return None

    with open(OTP_STORE_FILE, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            return None
    
    current_time = datetime.datetime.now()
    
    # Find the latest valid OTP for this user
    user_otps = [
        (otp_data["otp"], datetime.datetime.fromisoformat(otp_data["expires_at"]))
        for otp_id, otp_data in data.items()
        if otp_data.get("user_id") == user_id
    ]
    
    if not user_otps:
        return None
    
    # Get the most recent OTP that's still valid
    latest_otp, expiration = max(user_otps, key=lambda x: x[1])
    
    if expiration > current_time:
        return latest_otp
    
    return None