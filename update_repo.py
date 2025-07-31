#!/usr/bin/env python3
"""
Let's Talk Repository Update Script

This script helps update the entire repository to the latest configuration
and ensures all dependencies are properly installed.
"""

import os
import subprocess
import sys
import json

def run_command(command, description=""):
    """Run a shell command and return success status."""
    print(f"🔄 {description}")
    try:
        result = subprocess.run(command, shell=True, check=True, 
                            capture_output=True, text=True)
        print(f"✅ {description} - Success")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} - Failed")
        print(f"Error: {e.stderr}")
        return False

def main():
    """Main update function."""
    print("🚀 Let's Talk Repository Update")
    print("=" * 50)
    
    # Check Python version
    python_version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    print(f"📍 Python Version: {python_version}")
    
    if sys.version_info < (3, 10):
        print("⚠️  Warning: Python 3.10+ is recommended")
        return False
    
    # Create .env file if it doesn't exist
    if not os.path.exists('.env'):
        print("📋 Creating .env file from .env.example")
        try:
            with open('.env.example', 'r') as src, open('.env', 'w') as dst:
                dst.write(src.read())
            print("✅ Created .env file")
        except FileNotFoundError:
            print("⚠️  .env.example not found, skipping .env creation")
    
    # Update pip
    if not run_command("python -m pip install --upgrade pip", "Updating pip"):
        return False
    
    # Install core dependencies
    if not run_command("pip install -r requirements.txt", "Installing core dependencies"):
        return False
    
    # Install development dependencies
    if not run_command("pip install -r requirements-dev.txt", "Installing development dependencies"):
        return False
    
    # Run tests
    print("🧪 Running tests...")
    if run_command("python -m pytest tests/ -v", "Running test suite"):
        print("✅ All tests passed!")
    else:
        print("⚠️  Some tests failed - please check the output")
    
    # Run security checks
    print("🔒 Running security checks...")
    security_checks = [
        ("bandit -r src/", "Security linting with bandit"),
        ("safety check", "Dependency vulnerability check"),
        ("python -m pip_audit", "Package audit")
    ]
    
    for command, description in security_checks:
        run_command(command, description)
    
    print("\n🎉 Repository update completed!")
    print("\nNext steps:")
    print("1. Review the .env file and update any necessary values")
    print("2. Run 'python app.py' to start the application")
    print("3. Test the API endpoints using the provided curl examples")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)