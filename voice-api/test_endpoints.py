#!/usr/bin/env python3
"""
Endpoint Tester for Let's Talk API
Quick script to verify all endpoints are working
"""
import requests
import json
import time

BASE_URL = "http://localhost:5000"

def test_endpoint(method, path, data=None):
    """Test an endpoint and return status"""
    url = f"{BASE_URL}{path}"
    try:
        if method == "GET":
            response = requests.get(url)
        elif method == "POST":
            response = requests.post(url, json=data)
        
        print(f"✅ {method} {path} - Status: {response.status_code}")
        if response.status_code == 200:
            try:
                return response.json()
            except:
                return response.text
        else:
            return f"Error: {response.text}"
    except Exception as e:
        print(f"❌ {method} {path} - Error: {e}")
        return None

if __name__ == "__main__":
    print("🧪 Testing Let's Talk API Endpoints...")
    print("=" * 50)
    
    # Test basic endpoints
    health = test_endpoint("GET", "/health")
    print(f"Health Response: {health}")
    
    # Test OTP endpoint
    otp_data = {"phone_number": "+256700123456"}
    otp_response = test_endpoint("POST", "/calls/otp", otp_data)
    print(f"OTP Response: {otp_response}")
    
    # Test API tokens
    token_data = {"user_id": "test_user", "scopes": ["read", "write"]}
    token_response = test_endpoint("POST", "/api/tokens", token_data)
    print(f"Token Response: {token_response}")
    
    print("\n🌐 Web Dashboard: http://localhost:5000/api/tokens/dashboard")
    print("📝 Login Password: letstalk123")