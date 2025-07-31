"""
Utility functions for OTP (One-Time Password) generation.
"""
import secrets

def generate_otp():
    """
    Generate a cryptographically secure random 6-digit OTP (One-Time Password).
    Returns:
        str: A 6-digit OTP.
    """
    return str(secrets.randbelow(900000) + 100000)