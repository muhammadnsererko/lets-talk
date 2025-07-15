"""
Security utilities for local encryption, hashing, and secure random generation.
Implements AES-256 encryption/decryption, SHA-256 hashing, and random secret generation.
All logic is local-only and does not leak data externally.
"""
import os
import base64
import hashlib
import secrets
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.fernet import Fernet, InvalidToken

# Padding helpers for AES block size
BLOCK_SIZE = 128  # 128 bits for AES

def pad(data):
    padder = padding.PKCS7(BLOCK_SIZE).padder()
    return padder.update(data) + padder.finalize()

def unpad(data):
    unpadder = padding.PKCS7(BLOCK_SIZE).unpadder()
    return unpadder.update(data) + unpadder.finalize()

def derive_key(password: str, salt: bytes) -> bytes:
    # Derive a 32-byte key using PBKDF2 (AES-256)
    return hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100_000, dklen=32)

def encrypt_aes256(plaintext: bytes, password: str) -> bytes:
    salt = secrets.token_bytes(16)
    key = derive_key(password, salt)
    iv = secrets.token_bytes(16)
    padded_data = pad(plaintext)
    
    encryptor = Cipher(
        algorithms.AES(key),
        modes.CBC(iv)
    ).encryptor()
    
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()
    return base64.b64encode(salt + iv + ciphertext)

def decrypt_aes256(ciphertext_b64: bytes, password: str) -> bytes:
    raw = base64.b64decode(ciphertext_b64)
    salt, iv, ciphertext = raw[:16], raw[16:32], raw[32:]
    key = derive_key(password, salt)
    
    decryptor = Cipher(
        algorithms.AES(key),
        modes.CBC(iv)
    ).decryptor()
    
    padded_plaintext = decryptor.update(ciphertext) + decryptor.finalize()
    return unpad(padded_plaintext)

def sha256_hash_file(filepath: str) -> str:
    h = hashlib.sha256()
    with open(filepath, 'rb') as f:
        while True:
            chunk = f.read(4096)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()

def sha256_hash_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def generate_secure_token(length=32) -> str:
    return base64.urlsafe_b64encode(secrets.token_bytes(length)).decode('utf-8')

# Fernet helpers for strong symmetric encryption

def generate_fernet_key() -> bytes:
    """Generate a new Fernet key (base64-encoded 32 bytes)."""
    return Fernet.generate_key()

def encrypt_fernet(plaintext: bytes, key: bytes) -> bytes:
    """Encrypt data using Fernet symmetric encryption."""
    f = Fernet(key)
    return f.encrypt(plaintext)

def decrypt_fernet(ciphertext: bytes, key: bytes) -> bytes:
    """Decrypt Fernet-encrypted data. Raises InvalidToken if key is wrong or data is tampered."""
    f = Fernet(key)
    return f.decrypt(ciphertext)