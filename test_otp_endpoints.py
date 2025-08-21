# Test script to verify all OTP endpoints are working correctly using pytest and test_client.
# This tests the /api/otp/send, /calls/otp/verify, and /calls/otp/replay endpoints.

import pytest
import json
from app import app  # Assuming app is the Flask app instance

def test_otp_endpoints():
    client = app.test_client()
    
    # Test 1: Send OTP
    send_data = {"user_id": "test_user123"}
    response = client.post('/api/otp/send', json=send_data)
    assert response.status_code == 200
    send_result = response.get_json()
    otp_code = send_result.get("otp")
    assert otp_code is not None
    
    # Test 2: Verify OTP
    verify_data = {"user_id": "test_user123", "otp": otp_code}
    response = client.post('/calls/otp/verify', json=verify_data)
    assert response.status_code == 200
    verify_result = response.get_json()
    assert verify_result.get("message") == "OTP verified successfully"
    
    # Test 3: Replay OTP
    replay_data = {"user_id": "test_user123"}
    response = client.post('/calls/otp/replay', json=replay_data)
    assert response.status_code == 200
    replay_result = response.get_json()
    assert replay_result.get("message") == "OTP replayed"
    
    # Test 4: Invalid OTP verification
    invalid_data = {"user_id": "test_user123", "otp": "000000"}
    response = client.post('/calls/otp/verify', json=invalid_data)
    assert response.status_code == 400
    error_result = response.get_json()
    assert "Invalid OTP" in error_result.get("error")