"""
Security utilities for local encryption, hashing, and secure random generation.
Implements AES-256 encryption/decryption, SHA-256 hashing, and random secret generation.
All logic is local-only and does not leak data externally.
"""
import os
import base64
import hashlib
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from cryptography.fernet import Fernet, InvalidToken

# Padding helpers for AES block size
BLOCK_SIZE = 16

def pad(data):
    pad_len = BLOCK_SIZE - len(data) % BLOCK_SIZE
    return data + bytes([pad_len] * pad_len)

def unpad(data):
    pad_len = data[-1]
    if pad_len < 1 or pad_len > BLOCK_SIZE or data[-pad_len:] != bytes([pad_len] * pad_len):
        raise ValueError("Invalid padding.")
    return data[:-pad_len]

def derive_key(password: str, salt: bytes) -> bytes:
    # Derive a 32-byte key using PBKDF2 (AES-256)
    return hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100_000, dklen=32)

def encrypt_aes256(plaintext: bytes, password: str) -> bytes:
    salt = get_random_bytes(16)
    key = derive_key(password, salt)
    iv = get_random_bytes(16)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    ciphertext = cipher.encrypt(pad(plaintext))
    return base64.b64encode(salt + iv + ciphertext)

def decrypt_aes256(ciphertext_b64: bytes, password: str) -> bytes:
    raw = base64.b64decode(ciphertext_b64)
    salt, iv, ciphertext = raw[:16], raw[16:32], raw[32:]
    key = derive_key(password, salt)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return unpad(cipher.decrypt(ciphertext))

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
    return base64.urlsafe_b64encode(get_random_bytes(length)).decode('utf-8')

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