#!/usr/bin/env python3
"""
Let's Talk API - Complete Startup Script
This script handles installation, configuration, and server startup.
"""

import os
import sys
import subprocess
import base64
from pathlib import Path

def generate_fernet_key():
    """Generate a secure Fernet key"""
    key = base64.urlsafe_b64encode(os.urandom(32)).decode()
    return key

def generate_secret_key():
    """Generate a secure Flask secret key"""
    return base64.urlsafe_b64encode(os.urandom(32)).decode()

def install_dependencies():
    """Install all required dependencies"""
    print("📦 Installing dependencies...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                        check=True, capture_output=True, text=True)
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        print("💡 Trying alternative installation...")
        
        # Try installing packages one by one
        packages = [
            "Flask==3.0.0",
            "cryptography==41.0.7",
            "python-dotenv==1.0.0",
            "pyttsx3==2.90",
            "waitress==2.1.2",
            "requests"
        ]
        
        for package in packages:
            try:
                subprocess.run([sys.executable, "-m", "pip", "install", package], 
                                check=True, capture_output=True, text=True)
                print(f"✅ {package} installed")
            except subprocess.CalledProcessError as e:
                print(f"❌ Failed to install {package}: {e}")
                return False
        return True

def setup_environment():
    """Setup environment variables"""
    print("🔧 Setting up environment...")
    
    env_file = Path(".env")
    if not env_file.exists():
        print("Creating .env file...")
        with open(env_file, 'w') as f:
            f.write(f"""# Let's Talk API Environment Variables
FLASK_SECRET_KEY={generate_secret_key()}
FERNET_KEY={generate_fernet_key()}
ADMIN_PASSWORD=admin123

# AWS Configuration (optional)
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
AWS_REGION=us-east-1
""")
        print("✅ .env file created")
    else:
        print("✅ .env file already exists")

def check_port(port=5000):
    """Check if port is available"""
    import socket
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex(('localhost', port))
        sock.close()
        return result != 0
    except:
        return True

def start_server():
    """Start the Flask server"""
    print("🚀 Starting Let's Talk API server...")
    
    # Check if port 5000 is available
    if not check_port(5000):
        print("⚠️  Port 5000 is in use, trying port 5001...")
        port = 5001
    else:
        port = 5000
    
    # Import and start the server
    try:
        from app import app
        print(f"🌐 Server starting on http://localhost:{port}")
        print("📋 Available endpoints:")
        print(f"   • Health check: http://localhost:{port}/health")
        print(f"   • OTP endpoint: http://localhost:{port}/calls/otp")
        print(f"   • API tokens: http://localhost:{port}/api/tokens")
        print(f"   • Dashboard: http://localhost:{port}/api/tokens/dashboard")
        print("\n🔍 Testing endpoints...")
        
        # Test if server can start
        app.run(host='0.0.0.0', port=port, debug=True)
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("💡 Make sure all dependencies are installed")
        return False

def test_endpoints():
    """Test all endpoints"""
    import requests
    import time
    
    time.sleep(2)  # Wait for server to start
    
    base_url = "http://localhost:5000"
    endpoints = [
        "/health",
        "/api/tokens",
        "/calls/otp"
    ]
    
    print("\n🧪 Testing endpoints...")
    for endpoint in endpoints:
        try:
            response = requests.get(f"{base_url}{endpoint}", timeout=5)
            print(f"   ✅ {endpoint}: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"   ❌ {endpoint}: {e}")

def main():
    """Main startup function"""
    print("🎯 Let's Talk API - Complete Startup")
    print("=" * 40)
    
    # Change to project directory
    os.chdir(Path(__file__).parent)
    
    # Step 1: Install dependencies
    if not install_dependencies():
        print("❌ Cannot proceed without dependencies")
        return
    
    # Step 2: Setup environment
    setup_environment()
    
    # Step 3: Start server
    start_server()

if __name__ == "__main__":
    main()