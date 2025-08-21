import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Flask Configuration
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'
    PORT = int(os.environ.get('PORT', 5000))
    
    # Security Settings
    OTP_EXPIRY_MINUTES = int(os.environ.get('OTP_EXPIRY_MINUTES', 5))
    MAX_OTP_ATTEMPTS = int(os.environ.get('MAX_OTP_ATTEMPTS', 3))
    
    # Storage Settings
    OTP_STORE_FILE = os.environ.get('OTP_STORE_FILE') or 'otp_store.json'
    ANALYTICS_FILE = os.environ.get('ANALYTICS_FILE') or 'analytics_data.json'
    USER_SETTINGS_FILE = os.environ.get('USER_SETTINGS_FILE') or 'user_settings.json'
    
    # Voice Settings
    DEFAULT_VOICE_RATE = int(os.environ.get('DEFAULT_VOICE_RATE', 150))
    DEFAULT_VOICE_VOLUME = float(os.environ.get('DEFAULT_VOICE_VOLUME', 1.0))
    DEFAULT_VOICE_GENDER = os.environ.get('DEFAULT_VOICE_GENDER', 'female')
    
    # Development Settings
    READ_ONLY = os.environ.get('READ_ONLY', 'False').lower() == 'true'