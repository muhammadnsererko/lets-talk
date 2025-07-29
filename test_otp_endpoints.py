#!/usr/bin/env python3
"""
Test script to verify all OTP endpoints are working correctly.
This tests the /api/otp/send, /calls/otp/verify, and /calls/otp/replay endpoints.
"""

import requests
import json
import time

def test_otp_endpoints():
    base_url = "http://127.0.0.1:5000"
    
    print("🧪 Testing OTP API Endpoints...")
    print("=" * 50)
    
    # Test 1: Send OTP
    print("\n1. Testing /api/otp/send...")
    send_data = {"user_id": "test_user123"}
    try:
        response = requests.post(f"{base_url}/api/otp/send", json=send_data)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            send_result = response.json()
            print(f"   Response: {json.dumps(send_result, indent=2)}")
            otp_code = send_result.get("otp")
            print(f"   ✅ OTP Generated: {otp_code}")
        else:
            print(f"   ❌ Error: {response.text}")
            return False
    except Exception as e:
        print(f"   ❌ Connection Error: {e}")
        return False
    
    # Test 2: Verify OTP
    print("\n2. Testing /calls/otp/verify...")
    verify_data = {"user_id": "test_user123", "otp": otp_code}
    try:
        response = requests.post(f"{base_url}/calls/otp/verify", json=verify_data)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            verify_result = response.json()
            print(f"   Response: {json.dumps(verify_result, indent=2)}")
            print(f"   ✅ OTP Verified Successfully")
        else:
            print(f"   ❌ Error: {response.text}")
    except Exception as e:
        print(f"   ❌ Connection Error: {e}")
    
    # Test 3: Replay OTP
    print("\n3. Testing /calls/otp/replay...")
    replay_data = {"user_id": "test_user123"}
    try:
        response = requests.post(f"{base_url}/calls/otp/replay", json=replay_data)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            replay_result = response.json()
            print(f"   Response: {json.dumps(replay_result, indent=2)}")
            print(f"   ✅ OTP Replayed Successfully")
        else:
            print(f"   ❌ Error: {response.text}")
    except Exception as e:
        print(f"   ❌ Connection Error: {e}")
    
    # Test 4: Invalid OTP verification
    print("\n4. Testing invalid OTP verification...")
    invalid_data = {"user_id": "test_user123", "otp": "000000"}
    try:
        response = requests.post(f"{base_url}/calls/otp/verify", json=invalid_data)
        print(f"   Status: {response.status_code}")
        if response.status_code == 400:
            error_result = response.json()
            print(f"   Response: {json.dumps(error_result, indent=2)}")
            print(f"   ✅ Invalid OTP properly rejected")
        else:
            print(f"   ❌ Expected 400, got {response.status_code}")
    except Exception as e:
        print(f"   ❌ Connection Error: {e}")
    
    print("\n" + "=" * 50)
    print("✅ All OTP endpoint tests completed!")

if __name__ == "__main__":
    test_otp_endpoints()