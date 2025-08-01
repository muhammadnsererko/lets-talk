#!/usr/bin/env python3
"""
Voice API - Comprehensive Diagnostic and Fix Tool
This script automatically diagnoses and fixes common issues in the voice API project.
"""

import os
import sys
import subprocess
import json
import logging
from pathlib import Path

class VoiceAPIDiagnostic:
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.issues = []
        self.fixes = []
        
        # Set up logging
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger(__name__)
    
    def log_issue(self, issue):
        self.issues.append(issue)
        self.logger.error(f"❌ {issue}")
    
    def log_fix(self, fix):
        self.fixes.append(fix)
        self.logger.info(f"✅ {fix}")
    
    def check_python_environment(self):
        """Check Python version and environment"""
        self.logger.info("🔍 Checking Python environment...")
        
        # Check Python version
        version = sys.version_info
        if version.major < 3 or (version.major == 3 and version.minor < 7):
            self.log_issue(f"Python {version.major}.{version.minor} is too old (need 3.7+)")
            return False
        
        self.logger.info(f"✅ Python {version.major}.{version.minor}.{version.micro}")
        return True
    
    def fix_project_structure(self):
        """Fix project structure issues"""
        self.logger.info("🏗️ Fixing project structure...")
        
        # Create missing __init__.py files
        init_files = [
            "blueprints/__init__.py",
            "utils/__init__.py"
        ]
        
        for init_file in init_files:
            file_path = self.project_root / init_file
            if not file_path.exists():
                file_path.parent.mkdir(parents=True, exist_ok=True)
                file_path.write_text('"""Auto-generated __init__.py"""\n')
                self.log_fix(f"Created {init_file}")
            else:
                self.logger.info(f"✅ {init_file} already exists")
    
    def fix_dependencies(self):
        """Install missing dependencies"""
        self.logger.info("📦 Checking dependencies...")
        
        requirements_file = self.project_root / "requirements.txt"
        if not requirements_file.exists():
            self.log_issue("requirements.txt not found")
            return False
        
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", "-r", str(requirements_file)], 
                         check=True, capture_output=True, text=True)
            self.log_fix("Dependencies installed successfully")
            return True
        except subprocess.CalledProcessError as e:
            self.log_issue(f"Failed to install dependencies: {e}")
            return False
    
    def fix_environment_variables(self):
        """Create and configure environment variables"""
        self.logger.info("🔐 Setting up environment variables...")
        
        env_file = self.project_root / ".env"
        
        # Generate secure keys
        import secrets
        import base64
        
        secret_key = secrets.token_urlsafe(32)
        fernet_key = base64.urlsafe_b64encode(secrets.token_bytes(32)).decode()
        
        env_content = f"""# Voice API Environment Variables
# Generated on: {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

# Flask Configuration
SECRET_KEY={secret_key}
FLASK_SECRET_KEY={secret_key}
FLASK_ENV=development

# Security Keys
FERNET_KEY={fernet_key}
ADMIN_PASSWORD=admin123

# Server Configuration
PORT=5000
HOST=0.0.0.0

# Logging
LOG_LEVEL=INFO

# Optional AWS Configuration
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
AWS_REGION=us-east-1
"""
        
        if not env_file.exists():
            env_file.write_text(env_content)
            self.log_fix("Created .env file with secure keys")
        else:
            self.logger.info("✅ .env file already exists")
    
    def create_startup_script(self):
        """Create a startup script"""
        self.logger.info("📝 Creating startup script...")
        
        startup_script = f"""#!/usr/bin/env python3
# Voice API - Auto Startup Script
# Run this script to start the API server

import os
import sys
import subprocess
from pathlib import Path

# Change to project directory
os.chdir(r"{self.project_root}")

print("🎯 Voice API - Starting...")
print("=" * 50)

# Load environment variables
try:
    from dotenv import load_dotenv
    load_dotenv()
    print("✅ Environment variables loaded")
except ImportError:
    print("⚠️ python-dotenv not found, skipping environment loading")

# Start the server
print("🚀 Starting Flask server...")
print("📋 Available endpoints:")
print("   • Health check: http://localhost:5000/health")
print("   • OTP endpoint: http://localhost:5000/calls/otp")
print("   • API tokens: http://localhost:5000/api/tokens")
print("   • Dashboard: http://localhost:5000/api/tokens/dashboard")
print()

try:
    from server import main
    main()
except KeyboardInterrupt:
    print("\\n👋 Server stopped by user")
except Exception as e:
    print(f"❌ Error starting server: {e}")
    print("💡 Trying fallback method...")
    try:
        from app import app
        app.run(host='0.0.0.0', port=5000, debug=True)
    except Exception as e2:
        print(f"❌ Fallback also failed: {e2}")
"""
        
        startup_file = self.project_root / "start.py"
        with open(startup_file, 'w') as f:
            f.write(startup_script)
            
        self.log_fix("Created startup script: start.py")
    
    def run_full_diagnosis(self):
        """Run complete diagnosis and fix process"""
        self.logger.info("🔍 Starting comprehensive diagnosis...")
        
        # Step 1: Check Python environment
        self.check_python_environment()
        
        # Step 2: Fix project structure
        self.fix_project_structure()
        
        # Step 3: Fix dependencies
        self.fix_dependencies()
        
        # Step 4: Fix environment variables
        self.fix_environment_variables()
        
        # Step 5: Create startup script
        self.create_startup_script()
        
        # Generate report
        self.generate_report()
        
        return True
    
    def generate_report(self):
        """Generate diagnostic report"""
        report = {
            "diagnosis_time": str(__import__('datetime').datetime.now()),
            "issues_found": len(self.issues),
            "fixes_applied": len(self.fixes),
            "next_steps": [
                "Run 'python start.py' to start the server",
                "Visit http://localhost:5000/health to test",
                "Check app.log for any runtime issues"
            ]
        }
        
        report_file = self.project_root / "diagnostic_report.json"
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        self.logger.info(f"📊 Diagnostic report saved to: {report_file}")

if __name__ == "__main__":
    diagnostic = VoiceAPIDiagnostic()
    diagnostic.run_full_diagnosis()