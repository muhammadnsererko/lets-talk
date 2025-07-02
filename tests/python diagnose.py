import os
import sys
import platform
import subprocess
import json
import importlib.util
from pathlib import Path

report = []

def log(section, value):
    report.append(f"[{section}]\n{value}\n")

def check_python_version():
    log("Python Version", sys.version)

def check_installed_packages():
    try:
        output = subprocess.check_output([sys.executable, "-m", "pip", "freeze"])
        packages = output.decode().strip()
        log("Installed Packages", packages)
    except Exception as e:
        log("Installed Packages", f"Error: {e}")

def check_tests_folder():
    path = Path("tests")
    if path.exists() and path.is_dir():
        init_file = path / "__init__.py"
        if init_file.exists():
            log("Tests Folder", "Found with __init__.py (GOOD ✅)")
        else:
            log("Tests Folder", "Found, but missing __init__.py (BAD ❌)")
    else:
        log("Tests Folder", "Not found ❌")

def check_test_api_file():
    try:
        with open("tests/test_api.py", "r", encoding="utf-8") as f:
            content = f.read()
        compile(content, "tests/test_api.py", "exec")
        log("test_api.py Syntax", "No syntax errors ✅")
    except Exception as e:
        log("test_api.py Syntax", f"Syntax error ❌: {e}")

def check_test_discovery():
    try:
        result = subprocess.run(
            [sys.executable, "-m", "unittest", "discover"],
            capture_output=True, text=True, timeout=10
        )
        log("Test Discovery Output", result.stdout + result.stderr)
    except subprocess.TimeoutExpired:
        log("Test Discovery Output", "Timeout expired ❌")

def check_execution_policy():
    if platform.system() == "Windows":
        try:
            output = subprocess.check_output(
                ["powershell", "-Command", "Get-ExecutionPolicy"],
                stderr=subprocess.STDOUT,
                text=True
            )
            log("PowerShell Execution Policy", output.strip())
        except Exception as e:
            log("PowerShell Execution Policy", f"Error: {e}")

def check_permissions():
    try:
        test_file = Path("permission_test.txt")
        test_file.write_text("testing...")
        test_file.unlink()
        log("Filesystem Write Access", "Write & delete successful ✅")
    except Exception as e:
        log("Filesystem Write Access", f"❌ Error: {e}")

def suggest_fixes():
    suggestions = []

    if not Path("tests/__init__.py").exists():
        suggestions.append("- Add an empty `__init__.py` inside `tests/` folder.")

    if not Path("tests/test_api.py").exists():
        suggestions.append("- Ensure `tests/test_api.py` exists and starts with `test_` functions.")

    suggestions.append("- Run `python -m unittest discover` from the **project root folder**, not inside system folders.")
    suggestions.append("- Avoid using `requests` in tests — use Flask's test client instead.")
    suggestions.append("- If on Windows, ensure PowerShell allows scripts: `Set-ExecutionPolicy -Scope CurrentUser Bypass`.")

    log("Suggested Fixes", "\n".join(suggestions))

def write_report():
    with open("diagnostic_report.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(report))
    print("✅ Diagnostic complete. See 'diagnostic_report.txt' for details.")

def main():
    print("🔍 Running Diagnostic Agent...")
    check_python_version()
    check_installed_packages()
    check_tests_folder()
    check_test_api_file()
    check_test_discovery()
    check_execution_policy()
    check_permissions()
    suggest_fixes()
    write_report()

if __name__ == "__main__":
    main()
