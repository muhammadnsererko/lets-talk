"""
Security utilities for Let's Talk API
Handles encryption, hashing, and secure token generation
"""
import os
import secrets
import hashlib
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64

def generate_secure_token(length=32):
    """Generate a cryptographically secure random token"""
    return secrets.token_urlsafe(length)

def generate_fernet_key():
    """Generate a new Fernet encryption key"""
    return Fernet.generate_key()

def encrypt_fernet(data, key):
    """Encrypt data using Fernet symmetric encryption"""
    f = Fernet(key)
    return f.encrypt(data)

def decrypt_fernet(encrypted_data, key):
    """Decrypt data using Fernet symmetric encryption"""
    f = Fernet(key)
    return f.decrypt(encrypted_data)

def hash_password(password, salt=None):
    """Hash a password with salt using PBKDF2"""
    if salt is None:
        salt = os.urandom(32)
    
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    key = kdf.derive(password.encode())
    return salt + key

def verify_password(password, hashed):
    """Verify a password against its hash"""
    salt = hashed[:32]
    stored_key = hashed[32:]
    
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    
    try:
        kdf.verify(password.encode(), stored_key)
        return True
    except Exception:
        return False

def sha256_hash(data):
    """Generate SHA256 hash of input data"""
    if isinstance(data, str):
        data = data.encode()
    return hashlib.sha256(data).hexdigest()

def aes_encrypt_key_from_password(password, salt=None):
    """Generate AES encryption key from password using PBKDF2"""
    if salt is None:
        salt = os.urandom(16)
    
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
    return key, salt