#!/usr/bin/env python3
"""
Integration test for OTP endpoints using Flask test client.
This tests all OTP functionality without external dependencies.
"""

import sys
import os
import json

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app import app

def test_otp_integration():
    """Test complete OTP flow using Flask test client"""
    
    print("🔍 Running OTP Integration Tests...")
    print("=" * 50)
    
    with app.test_client() as client:
        user_id = "integration_test_user"
        
        # Test 1: Send OTP
        print("\n1. Testing /api/otp/send...")
        response = client.post('/api/otp/send', json={'user_id': user_id})
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.get_json()
            print(f"   Response: {json.dumps(data, indent=2)}")
            if data.get('status') == 'success' and 'otp' in data:
                otp_code = data['otp']
                print(f"   ✅ OTP Generated: {otp_code}")
                
                # Test 2: Verify OTP
                print("\n2. Testing /calls/otp/verify...")
                verify_response = client.post('/calls/otp/verify', json={
                    'user_id': user_id,
                    'otp': otp_code
                })
                print(f"   Status: {verify_response.status_code}")
                verify_data = verify_response.get_json()
                print(f"   Response: {json.dumps(verify_data, indent=2)}")
                
                if verify_response.status_code == 200 and verify_data.get('status') == 'success':
                    print("   ✅ OTP Verified Successfully")
                else:
                    print("   ❌ OTP Verification Failed")
                
                # Test 3: Replay OTP
                print("\n3. Testing /calls/otp/replay...")
                replay_response = client.post('/calls/otp/replay', json={
                    'user_id': user_id
                })
                print(f"   Status: {replay_response.status_code}")
                replay_data = replay_response.get_json()
                print(f"   Response: {json.dumps(replay_data, indent=2)}")
                
                if replay_response.status_code == 200 and replay_data.get('status') == 'success':
                    print("   ✅ OTP Replay Successful")
                else:
                    print("   ❌ OTP Replay Failed")
                
                # Test 4: Invalid OTP
                print("\n4. Testing invalid OTP verification...")
                invalid_response = client.post('/calls/otp/verify', json={
                    'user_id': user_id,
                    'otp': '000000'
                })
                print(f"   Status: {invalid_response.status_code}")
                invalid_data = invalid_response.get_json()
                print(f"   Response: {json.dumps(invalid_data, indent=2)}")
                
                if invalid_response.status_code == 400:
                    print("   ✅ Invalid OTP properly rejected")
                else:
                    print("   ❌ Invalid OTP test failed")
                    
            else:
                print("   ❌ Invalid response format")
        else:
            print(f"   ❌ Send OTP failed: {response.get_json()}")
    
    print("\n" + "=" * 50)
    print("✅ Integration test completed!")

if __name__ == "__main__":
    test_otp_integration()