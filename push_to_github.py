#!/usr/bin/env python3
"""
Push voice-api repository to GitHub
Target: https://github.com/muhammadnsererko/lets-talk
"""

import os
import subprocess
import sys

def run_command(cmd, cwd=None):
    """Run a shell command and return the result"""
    try:
        result = subprocess.run(
            cmd, 
            shell=True, 
            capture_output=True, 
            text=True, 
            cwd=cwd
        )
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def main():
    repo_path = os.path.dirname(os.path.abspath(__file__))
    
    print("🚀 Starting push to GitHub...")
    print(f"📁 Repository path: {repo_path}")
    
    # Change to repository directory
    os.chdir(repo_path)
    
    # Step 1: Initialize git if not already done
    print("\n📦 Initializing git repository...")
    success, stdout, stderr = run_command("git init")
    if success:
        print("✅ Git repository initialized")
    else:
        if "already exists" in stderr.lower():
            print("✅ Git repository already exists")
        else:
            print(f"❌ Failed to initialize git: {stderr}")
            return False
    
    # Step 2: Add remote repository
    print("\n🔗 Adding remote repository...")
    commands = [
        "git remote remove origin",
        "git remote add origin https://github.com/muhammadnsererko/lets-talk.git"
    ]
    
    for cmd in commands:
        success, stdout, stderr = run_command(cmd)
        if success or "Could not remove config section" in stderr:
            continue
    
    # Verify remote was added
    success, stdout, stderr = run_command("git remote -v")
    if success and "muhammadnsererko/lets-talk" in stdout:
        print("✅ Remote repository configured")
    else:
        print(f"❌ Failed to configure remote: {stderr}")
        return False
    
    # Step 3: Add all files
    print("\n➕ Adding all files...")
    success, stdout, stderr = run_command("git add .")
    if success:
        print("✅ All files added to staging")
    else:
        print(f"❌ Failed to add files: {stderr}")
        return False
    
    # Step 4: Commit with comprehensive message
    print("\n💾 Creating commit...")
    commit_message = """Initial commit: Voice API with OTP & Token Authentication

Features:
- ✅ OTP Generation & Verification
- ✅ API Token Authentication
- ✅ Health Check Endpoints
- ✅ Security & Rate Limiting
- ✅ Complete Test Suite (27 tests)
- ✅ Clean Repository Structure

Structure:
- Modular Flask blueprints
- Organized utilities
- Comprehensive testing
- Production-ready configuration

Ready for deployment!"""
    
    cmd = f'git commit -m "{commit_message}"'
    success, stdout, stderr = run_command(cmd)
    if success:
        print("✅ Commit created successfully")
    elif "nothing to commit" in stderr.lower():
        print("✅ Nothing to commit (repository already up to date)")
    else:
        print(f"❌ Failed to commit: {stderr}")
        return False
    
    # Step 5: Push to GitHub
    print("\n🚀 Pushing to GitHub...")
    print("This may take a moment...")
    
    success, stdout, stderr = run_command("git push -u origin main")
    if success:
        print("✅ Successfully pushed to GitHub!")
        print(f"🌐 Repository: https://github.com/muhammadnsererko/lets-talk")
        return True
    elif "failed to push" in stderr.lower() or "permission denied" in stderr.lower():
        print("\n⚠️  Push failed - likely authentication issue")
        print("\n🔧 Manual push commands:")
        print("1. Check your GitHub credentials")
        print("2. Run these commands manually:")
        print("   git remote set-url origin https://github.com/muhammadnsererko/lets-talk.git")
        print("   git branch -M main")
        print("   git push -u origin main")
        return False
    else:
        print(f"⚠️  Push issues: {stderr}")
        print("\n🔧 Try manual push with:")
        print("   git push -f origin main")
        return False

if __name__ == "__main__":
    print("🎯 Voice API Push to GitHub")
    print("=" * 40)
    
    success = main()
    
    if success:
        print("\n🎉 Repository successfully pushed to GitHub!")
        print("📍 https://github.com/muhammadnsererko/lets-talk")
    else:
        print("\n📋 Manual steps provided above")
        print("🔄 You can also use: git push -u origin main")
    
    input("\nPress Enter to continue...")