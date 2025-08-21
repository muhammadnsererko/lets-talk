#!/usr/bin/env python3
"""
Comprehensive test script for API token functionality
"""
import requests
import json
import sys
import os
import subprocess
import time

# Configuration
BASE_URL = "http://localhost:5000"

class APITokenTester:
    def __init__(self, base_url):
        self.base_url = base_url
        self.token = None
    
    def test_health_check(self):
        """Test health check endpoint"""
        print("Testing health check...")
        try:
            response = requests.get(f"{self.base_url}/health")
            if response.status_code == 200:
                data = response.json()
                if data.get('status') == 'healthy':
                    print("✓ Health check passed")
                    return True
                else:
                    print("✗ Health check failed - unhealthy status")
                    return False
            else:
                print(f"✗ Health check failed - status {response.status_code}")
                return False
        except Exception as e:
            print(f"✗ Health check failed - {e}")
            return False
    
    def test_create_token(self):
        """Test API token creation"""
        print("Testing token creation...")
        try:
            payload = {"name": "test-token"}
            response = requests.post(f"{self.base_url}/api/tokens", json=payload)
            
            if response.status_code == 201:
                data = response.json()
                self.token = data.get('token')
                if self.token:
                    print("✓ Token creation passed")
                    print(f"  Token: {self.token[:10]}...")
                    return True
                else:
                    print("✗ Token creation failed - no token returned")
                    return False
            else:
                print(f"✗ Token creation failed - status {response.status_code}")
                print(f"  Response: {response.text}")
                return False
        except Exception as e:
            print(f"✗ Token creation failed - {e}")
            return False
    
    def test_validate_token(self):
        """Test token validation"""
        print("Testing token validation...")
        if not self.token:
            print("✗ Token validation failed - no token to test")
            return False
        
        try:
            payload = {"token": self.token}
            response = requests.post(f"{self.base_url}/api/tokens/validate", json=payload)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('valid'):
                    print("✓ Token validation passed")
                    return True
                else:
                    print("✗ Token validation failed - invalid token")
                    return False
            else:
                print(f"✗ Token validation failed - status {response.status_code}")
                return False
        except Exception as e:
            print(f"✗ Token validation failed - {e}")
            return False
    
    def test_list_tokens(self):
        """Test listing tokens (requires authentication)"""
        print("Testing token listing...")
        if not self.token:
            print("✗ Token listing failed - no token to test")
            return False
        
        try:
            headers = {"Authorization": f"Bearer {self.token}"}
            response = requests.get(f"{self.base_url}/api/tokens", headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                tokens = data.get('tokens', [])
                print(f"✓ Token listing passed - found {len(tokens)} tokens")
                return True
            else:
                print(f"✗ Token listing failed - status {response.status_code}")
                return False
        except Exception as e:
            print(f"✗ Token listing failed - {e}")
            return False
    
    def test_invalid_token(self):
        """Test invalid token handling"""
        print("Testing invalid token handling...")
        try:
            payload = {"token": "invalid-token-12345"}
            response = requests.post(f"{self.base_url}/api/tokens/validate", json=payload)
            
            if response.status_code == 404:
                print("✓ Invalid token handling passed")
                return True
            else:
                print(f"✗ Invalid token handling failed - status {response.status_code}")
                return False
        except Exception as e:
            print(f"✗ Invalid token handling failed - {e}")
            return False

def start_flask_app():
    """Start the Flask app in the background"""
    print("Starting Flask application...")
    cmd = [sys.executable, "-c", """
import sys
import os
sys.path.insert(0, os.getcwd())
from app import app
app.run(host='0.0.0.0', port=5000, debug=False)
"""]
    
    # Start the process
    process = subprocess.Popen(cmd, cwd=os.getcwd(), 
                               stdout=subprocess.DEVNULL, 
                               stderr=subprocess.DEVNULL)
    
    # Wait a moment for the server to start
    time.sleep(3)
    return process

def main():
    """Run all API token tests"""
    print("=" * 50)
    print("API Token Functionality Test Suite")
    print("=" * 50)
    
    # Start Flask app
    flask_process = start_flask_app()
    
    try:
        # Initialize tester
        tester = APITokenTester(BASE_URL)
        
        # Run tests
        tests = [
            tester.test_health_check,
            tester.test_create_token,
            tester.test_validate_token,
            tester.test_list_tokens,
            tester.test_invalid_token
        ]
        
        passed = 0
        total = len(tests)
        
        for test in tests:
            if test():
                passed += 1
            print()
        
        # Summary
        print("=" * 50)
        print(f"Test Results: {passed}/{total} tests passed")
        
        if passed == total:
            print("🎉 All tests passed! API token functionality is working correctly.")
            return True
        else:
            print("❌ Some tests failed. Check the output above for details.")
            return False
            
    finally:
        # Clean up
        flask_process.terminate()
        flask_process.wait()

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)