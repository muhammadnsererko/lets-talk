# Before:
import random

def generate_otp():
    return random.randint(100000, 999999)

# After:
import secrets

def generate_otp():
    return ''.join(str(secrets.randbelow(10)) for _ in range(6))