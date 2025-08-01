#!/usr/bin/env python3
"""
Test script for Let's Talk API endpoints
"""
import requests
import json

def test_endpoint(url, method='GET', data=None):
    """Test an API endpoint"""
    try:
        headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
        
        if method.upper() == 'GET':
            response = requests.get(url, headers=headers, timeout=10)
        elif method.upper() == 'POST':
            response = requests.post(url, json=data, headers=headers, timeout=10)
        else:
            raise ValueError(f"Unsupported method: {method}")
            
        print(f"✅ {method} {url}")
        print(f"Status: {response.status_code}")
        
        try:
            json_response = response.json()
            print(f"Response: {json.dumps(json_response, indent=2)}")
        except:
            print(f"Raw response: {response.text}")
            
        return response.status_code == 200
        
    except Exception as e:
        print(f"❌ Error testing {url}: {e}")
        return False

if __name__ == "__main__":
    base_url = "http://localhost:5000"
    
    print("🔍 Testing Let's Talk API Endpoints")
    print("=" * 50)
    
    # Test health endpoint
    test_endpoint(f"{base_url}/health")
    
    print("\n" + "=" * 50)
    
    # Test OTP generation
    test_endpoint(f"{base_url}/calls/otp", method='POST', data={
        "phone_number": "+256700123456"
    })
    
    print("\n" + "=" * 50)
    
    # Test API token creation
    test_endpoint(f"{base_url}/api/tokens", method='POST', data={
        "user_id": "test_user",
        "scopes": ["read", "write"]
    })
    
    print("\n" + "=" * 50)
    print("🎯 Testing complete!")