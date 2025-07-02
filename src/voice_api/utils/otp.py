"""
Utility functions for OTP (One-Time Password) generation.
"""
import random

def generate_otp():
    """
    Generate a random 6-digit OTP (One-Time Password).
    Returns:
        int: A 6-digit OTP.
    """
    return random.randint(100000, 999999)