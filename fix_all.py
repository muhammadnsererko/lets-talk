#!/usr/bin/env python3
"""
Voice API - Complete Diagnostic and Fix Tool
This script diagnoses and fixes all common issues in the voice API project.
"""

import os
import sys
import subprocess
import json
from pathlib import Path

class VoiceAPIFixer:
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.issues_found = []
        self.issues_fixed = []
    
    def log_issue(self, issue, fixed=False):
        if fixed:
            self.issues_fixed.append(issue)
        else:
            self.issues_found.append(issue)
        print(f"{'✅ FIXED' if fixed else '❌ ISSUE'}: {issue}")
    
    def check_python_version(self):
        """Check Python version compatibility."""
        version = sys.version_info
        if version.major < 3 or (version.major == 3 and version.minor < 7):
            self.log_issue(f"Python {version.major}.{version.minor} is too old. Need 3.7+")
            return False
        print(f"✅ Python {version.major}.{version.minor} is compatible")
        return True
    
    def check_dependencies(self):
        """Check and install required dependencies."""
        requirements = [
            "Flask==3.0.0",
            "cryptography==41.0.7",
            "python-dotenv==1.0.0",
            "pyttsx3==2.90",
            "waitress==2.1.2",
            "requests"
        ]
        
        missing_packages = []
        for package in requirements:
            package_name = package.split("==")[0]
            try:
                __import__(package_name.lower().replace("-", "_"))
                print(f"✅ {package_name} is installed")
            except ImportError:
                missing_packages.append(package)
                self.log_issue(f"Missing package: {package_name}")
        
        if missing_packages:
            print("Installing missing packages...")
            try:
                subprocess.run([sys.executable, "-m", "pip", "install"] + missing_packages, check=True)
                self.log_issue(f"Installed {len(missing_packages)} packages", fixed=True)
            except subprocess.CalledProcessError as e:
                self.log_issue(f"Failed to install packages: {e}")
    
    def check_project_structure(self):
        """Check and fix project structure."""
        required_files = {
            "app.py": "Main Flask application",
            "server.py": "Server startup script",
            "requirements.txt": "Dependencies list",
            "blueprints/__init__.py": "Blueprints package init",
            "blueprints/otp.py": "OTP blueprint",
            "blueprints/api_tokens.py": "API tokens blueprint",
            "utils/__init__.py": "Utils package init",
            "utils/security.py": "Security utilities",
            "templates/dashboard.html": "Dashboard template",
            ".env": "Environment variables"
        }
        
        for file_path, description in required_files.items():
            full_path = self.project_root / file_path
            if not full_path.exists():
                self.log_issue(f"Missing file: {file_path} ({description})")
                
                # Create missing __init__.py files
                if file_path.endswith("__init__.py"):
                    full_path.parent.mkdir(parents=True, exist_ok=True)
                    full_path.write_text('"""Auto-generated __init__.py"""')
                    self.log_issue(f"Created: {file_path}", fixed=True)
            else:
                print(f"✅ Found: {file_path}")
    
    def check_environment_variables(self):
        """Check and fix environment variables."""
        env_file = self.project_root / ".env"
        required_vars = {
            "FLASK_SECRET_KEY": "your-secret-key-here",
            "FERNET_KEY": "your-fernet-key-here",
            "ADMIN_PASSWORD": "admin123",
            "AWS_ACCESS_KEY_ID": "your-aws-key",
            "AWS_SECRET_ACCESS_KEY": "your-aws-secret",
            "AWS_REGION": "us-east-1"
        }
        
        if not env_file.exists():
            self.log_issue("Missing .env file")
            
            # Generate secure keys
            import secrets
            fernet_key = secrets.token_urlsafe(32)
            flask_key = secrets.token_urlsafe(32)
            
            env_content = f"""FLASK_SECRET_KEY={flask_key}
FERNET_KEY={fernet_key}
ADMIN_PASSWORD=admin123
AWS_ACCESS_KEY_ID=your-aws-key
AWS_SECRET_ACCESS_KEY=your-aws-secret
AWS_REGION=us-east-1
"""
            env_file.write_text(env_content)
            self.log_issue("Created .env file with generated keys", fixed=True)
        else:
            content = env_file.read_text()
            for var in required_vars:
                if var not in content:
                    self.log_issue(f"Missing environment variable: {var}")
                    
                    if var == "FLASK_SECRET_KEY":
                        import secrets
                        new_key = secrets.token_urlsafe(32)
                        with open(env_file, "a") as f:
                            f.write(f"\nFLASK_SECRET_KEY={new_key}\n")
                        self.log_issue(f"Added FLASK_SECRET_KEY", fixed=True)
                    elif var == "FERNET_KEY":
                        import secrets
                        new_key = secrets.token_urlsafe(32)
                        with open(env_file, "a") as f:
                            f.write(f"\nFERNET_KEY={new_key}\n")
                        self.log_issue(f"Added FERNET_KEY", fixed=True)
                else:
                    print(f"✅ Found env var: {var}")
    
    def check_port_availability(self, port=5000):
        """Check if port is available."""
        import socket
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                result = s.connect_ex(('localhost', port))
                if result == 0:
                    self.log_issue(f"Port {port} is already in use")
                    return False
                else:
                    print(f"✅ Port {port} is available")
                    return True
        except Exception as e:
            self.log_issue(f"Error checking port {port}: {e}")
            return False
    
    def generate_report(self):
        """Generate diagnostic report."""
        report = {
            "issues_found": len(self.issues_found),
            "issues_fixed": len(self.issues_fixed),
            "issues": {
                "found": self.issues_found,
                "fixed": self.issues_fixed
            },
            "project_root": str(self.project_root),
            "python_version": f"{sys.version_info.major}.{sys.version_info.minor}"
        }
        
        report_file = self.project_root / "diagnostic_report.json"
        with open(report_file, "w") as f:
            json.dump(report, f, indent=2)
        
        print(f"\n📊 Diagnostic report saved to: {report_file}")
        return report
    
    def fix_all_issues(self):
        """Run complete diagnostic and fix process."""
        print("🔍 Starting Voice API diagnostic...")
        print("=" * 50)
        
        self.check_python_version()
        self.check_dependencies()
        self.check_project_structure()
        self.check_environment_variables()
        self.check_port_availability()
        
        print("\n" + "=" * 50)
        print("📋 DIAGNOSTIC COMPLETE")
        print(f"Issues found: {len(self.issues_found)}")
        print(f"Issues fixed: {len(self.issues_fixed)}")
        
        if self.issues_found:
            print("\n❌ Issues still present:")
            for issue in self.issues_found:
                if issue not in self.issues_fixed:
                    print(f"  - {issue}")
        
        if self.issues_fixed:
            print("\n✅ Issues successfully fixed:")
            for issue in self.issues_fixed:
                print(f"  - {issue}")
        
        return self.generate_report()
    
    def start_server(self):
        """Start the Flask server."""
        print("\n🚀 Starting Voice API server...")
        try:
            subprocess.run([sys.executable, "server.py"], cwd=self.project_root)
        except KeyboardInterrupt:
            print("\n✅ Server stopped by user")
        except Exception as e:
            self.log_issue(f"Failed to start server: {e}")

if __name__ == "__main__":
    fixer = VoiceAPIFixer()
    
    if len(sys.argv) > 1 and sys.argv[1] == "start":
        fixer.start_server()
    else:
        report = fixer.fix_all_issues()
        
        if len(sys.argv) > 1 and sys.argv[1] == "fix-only":
            print("\n🔧 Fix-only mode complete. Run 'python fix_all.py start' to start server.")
        else:
            if not report["issues_found"] or len(report["issues_found"]) == len(report["issues_fixed"]):
                print("\n✅ All issues resolved! Starting server...")
                fixer.start_server()
            else:
                print("\n⚠️ Some issues remain. Please check the report and fix manually.")
                print("Run 'python fix_all.py start' to start server anyway.")