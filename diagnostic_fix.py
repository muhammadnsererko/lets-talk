#!/usr/bin/env python3
"""
Let's Talk API - Comprehensive Diagnostic and Fix Tool
This script diagnoses and fixes common issues in the Let's Talk API project.
"""

import os
import sys
import json
import subprocess
import importlib.util
from pathlib import Path

class DiagnosticTool:
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.issues_found = []
        self.fixes_applied = []
        
    def log_issue(self, issue, severity="INFO"):
        """Log an issue with severity level"""
        self.issues_found.append({"issue": issue, "severity": severity})
        print(f"[{severity}] {issue}")
        
    def log_fix(self, fix):
        """Log a fix that was applied"""
        self.fixes_applied.append(fix)
        print(f"[FIXED] {fix}")
        
    def check_python_version(self):
        """Check Python version compatibility"""
        version = sys.version_info
        if version.major < 3 or (version.major == 3 and version.minor < 7):
            self.log_issue(f"Python {version.major}.{version.minor} is too old. Requires 3.7+", "ERROR")
            return False
        return True
        
    def check_dependencies(self):
        """Check if all required dependencies are installed"""
        requirements_file = self.project_root / "requirements.txt"
        if not requirements_file.exists():
            self.log_issue("requirements.txt not found", "ERROR")
            return False
            
        with open(requirements_file) as f:
            requirements = f.read().splitlines()
            
        missing = []
        for req in requirements:
            if req.strip() and not req.startswith("#"):
                package_name = req.split("==")[0].split(">=")[0].split("<")[0]
                if not self.is_package_installed(package_name):
                    missing.append(package_name)
                    
        if missing:
            self.log_issue(f"Missing packages: {', '.join(missing)}", "ERROR")
            return False
        return True
        
    def is_package_installed(self, package_name):
        """Check if a package is installed"""
        try:
            spec = importlib.util.find_spec(package_name)
            return spec is not None
        except ImportError:
            return False
            
    def check_file_structure(self):
        """Check if all required files exist"""
        required_files = [
            "app.py",
            "server.py",
            "blueprints/otp.py",
            "blueprints/api_tokens.py",
            "utils/security.py",
            "templates/dashboard.html",
            "requirements.txt"
        ]
        
        missing_files = []
        for file_path in required_files:
            full_path = self.project_root / file_path
            if not full_path.exists():
                missing_files.append(file_path)
                
        if missing_files:
            self.log_issue(f"Missing files: {', '.join(missing_files)}", "ERROR")
            return False
        return True
        
    def check_blueprint_imports(self):
        """Check blueprint imports and fix __init__.py issues"""
        blueprints_dir = self.project_root / "blueprints"
        init_file = blueprints_dir / "__init__.py"
        
        if not init_file.exists():
            self.log_issue("Missing blueprints/__init__.py", "WARNING")
            try:
                init_file.touch()
                init_file.write_text('"""Blueprints package"""\n')
                self.log_fix("Created blueprints/__init__.py")
            except Exception as e:
                self.log_issue(f"Failed to create __init__.py: {e}", "ERROR")
                
    def check_environment_variables(self):
        """Check environment variables and .env file"""
        env_file = self.project_root / ".env"
        required_vars = [
            "FLASK_SECRET_KEY",
            "FERNET_KEY",
            "ADMIN_PASSWORD"
        ]
        
        missing_vars = []
        for var in required_vars:
            if not os.getenv(var):
                if not env_file.exists():
                    missing_vars.append(var)
                else:
                    with open(env_file) as f:
                        if var not in f.read():
                            missing_vars.append(var)
                            
        if missing_vars:
            self.log_issue(f"Missing environment variables: {', '.join(missing_vars)}", "WARNING")
            self.create_sample_env_file()
            
    def create_sample_env_file(self):
        """Create a sample .env file"""
        env_content = """# Let's Talk API Environment Variables
FLASK_SECRET_KEY=your-secret-key-here-change-this-in-production
FERNET_KEY=your-fernet-key-here-must-be-32-url-safe-base64-encoded
ADMIN_PASSWORD=admin123
"""
        env_file = self.project_root / ".env"
        if not env_file.exists():
            with open(env_file, 'w') as f:
                f.write(env_content)
            self.log_fix("Created .env file with sample configuration")
            
    def check_port_availability(self, port=5000):
        """Check if the port is available"""
        import socket
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            result = sock.connect_ex(('localhost', port))
            sock.close()
            if result == 0:
                self.log_issue(f"Port {port} is already in use", "WARNING")
                return False
        except Exception as e:
            self.log_issue(f"Error checking port {port}: {e}", "ERROR")
        return True
        
    def test_endpoints(self):
        """Test all API endpoints"""
        try:
            import requests
            base_url = "http://localhost:5000"
            
            # Test health endpoint
            try:
                response = requests.get(f"{base_url}/health", timeout=5)
                if response.status_code == 200:
                    self.log_fix("Health endpoint is working")
                else:
                    self.log_issue(f"Health endpoint returned {response.status_code}", "ERROR")
            except requests.exceptions.RequestException as e:
                self.log_issue(f"Health endpoint unreachable: {e}", "ERROR")
                
        except ImportError:
            self.log_issue("requests package not available for testing", "WARNING")
            
    def generate_fix_report(self):
        """Generate a comprehensive fix report"""
        report = {
            "issues_found": self.issues_found,
            "fixes_applied": self.fixes_applied,
            "recommendations": [
                "Run 'pip install -r requirements.txt' to install dependencies",
                "Set up environment variables in .env file",
                "Use 'python server.py --host 0.0.0.0 --port 5000' for development",
                "Test endpoints with: curl http://localhost:5000/health",
                "For production, use: python server.py --prod --host 0.0.0.0 --port 80"
            ]
        }
        
        report_file = self.project_root / "diagnostic_report.json"
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
            
        return report
        
    def run_all_checks(self):
        """Run all diagnostic checks"""
        print("🔍 Let's Talk API - Comprehensive Diagnostic")
        print("=" * 50)
        
        self.check_python_version()
        self.check_file_structure()
        self.check_dependencies()
        self.check_blueprint_imports()
        self.check_environment_variables()
        self.check_port_availability()
        
        print("\n" + "=" * 50)
        print("📋 Diagnostic Complete")
        
        if self.issues_found:
            print(f"❌ Found {len(self.issues_found)} issues")
        else:
            print("✅ No critical issues found")
            
        report = self.generate_fix_report()
        return report

def main():
    """Main diagnostic function"""
    tool = DiagnosticTool()
    report = tool.run_all_checks()
    
    if tool.issues_found:
        print("\n🔧 Issues Found:")
        for issue in tool.issues_found:
            print(f"  - {issue['severity']}: {issue['issue']}")
            
    if tool.fixes_applied:
        print("\n✅ Fixes Applied:")
        for fix in tool.fixes_applied:
            print(f"  - {fix}")
            
    print(f"\n📊 Full report saved to: diagnostic_report.json")
    
    # Provide next steps
    print("\n🚀 Next Steps:")
    print("1. Install missing dependencies: pip install -r requirements.txt")
    print("2. Configure environment variables in .env file")
    print("3. Start the server: python server.py --host 0.0.0.0 --port 5000")
    print("4. Test the API: curl http://localhost:5000/health")

if __name__ == "__main__":
    main()