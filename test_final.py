import requests
import json

def test_endpoints():
    base_url = "http://localhost:5000"
    
    print("Testing Voice API endpoints...")
    
    # Test health endpoint
    try:
        response = requests.get(f"{base_url}/health")
        print(f"✅ Health endpoint: {response.status_code} - {response.json()}")
    except Exception as e:
        print(f"❌ Health endpoint failed: {e}")
    
    # Test OTP endpoint
    try:
        payload = {
            "phone_number": "+1234567890",
            "message": "Your verification code is: 123456"
        }
        response = requests.post(f"{base_url}/calls/otp", json=payload)
        print(f"✅ OTP endpoint: {response.status_code} - {response.json()}")
    except Exception as e:
        print(f"❌ OTP endpoint failed: {e}")
    
    # Test tokens endpoint
    try:
        payload = {
            "password": "admin123"
        }
        response = requests.post(f"{base_url}/api/tokens", json=payload)
        print(f"✅ Tokens endpoint: {response.status_code} - {response.json()}")
    except Exception as e:
        print(f"❌ Tokens endpoint failed: {e}")

if __name__ == "__main__":
    test_endpoints()