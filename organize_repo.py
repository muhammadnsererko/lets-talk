#!/usr/bin/env python3
"""
Repository Organization Script
Cleans up and organizes the voice-api repository structure
"""
import os
import shutil
import glob
from pathlib import Path

def create_directory_structure():
    """Create clean directory structure"""
    directories = [
        'docs',
        'scripts',
        'tests',
        'src/voice_api',
        'blueprints',
        'config',
        'data',
        'logs'
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"Created directory: {directory}")

def organize_python_files():
    """Organize Python files into proper locations"""
    # Move blueprints to blueprints directory
    blueprint_files = ['otp.py', 'api_tokens.py']
    for file in blueprint_files:
        if os.path.exists(f'blueprints/{file}'):
            print(f"✓ {file} already in blueprints/")
        elif os.path.exists(file):
            shutil.move(file, f'blueprints/{file}')
            print(f"Moved {file} → blueprints/{file}")

def organize_config_files():
    """Organize configuration files"""
    config_files = ['config.py', 'requirements.txt', '.env.example']
    for file in config_files:
        if os.path.exists(file) and not os.path.exists(f'config/{file}'):
            shutil.move(file, f'config/{file}')
            print(f"Moved {file} → config/{file}")

def organize_documentation():
    """Organize documentation files"""
    doc_files = [
        'README.md', 'API_TOKENS_GUIDE.md', 'TESTING_SUMMARY.md',
        'FINAL_DIAGNOSTIC_REPORT.md'
    ]
    for file in doc_files:
        if os.path.exists(file) and not os.path.exists(f'docs/{file}'):
            shutil.move(file, f'docs/{file}')
            print(f"Moved {file} → docs/{file}")

def organize_test_files():
    """Organize test files"""
    test_files = [
        'test_api_tokens.py', 'final_test.py'
    ]
    for file in test_files:
        if os.path.exists(file) and not os.path.exists(f'scripts/{file}'):
            shutil.move(file, f'scripts/{file}')
            print(f"Moved {file} → scripts/{file}")

def clean_temporary_files():
    """Clean up temporary and backup files"""
    patterns = [
        '*.pyc',
        '__pycache__',
        '*.pyo',
        '*.pyd',
        '.DS_Store',
        'Thumbs.db',
        '*.tmp',
        '*.log'
    ]
    
    for pattern in patterns:
        files = glob.glob(f'**/{pattern}', recursive=True)
        for file in files:
            try:
                if os.path.isfile(file):
                    os.remove(file)
                    print(f"Removed: {file}")
                elif os.path.isdir(file):
                    shutil.rmtree(file)
                    print(f"Removed directory: {file}")
            except Exception as e:
                print(f"Could not remove {file}: {e}")

def create_readme():
    """Create a clean, organized README"""
    readme_content = """# Voice API

A secure voice authentication API with OTP generation and management capabilities.

## Project Structure

```
voice-api/
├── src/voice_api/          # Core application code
├── blueprints/            # Flask blueprints
│   ├── otp.py            # OTP generation and verification
│   └── api_tokens.py     # API token management
├── tests/                 # Test files
├── config/               # Configuration files
├── docs/                 # Documentation
├── scripts/              # Utility scripts
├── data/                 # Data storage
└── logs/                 # Log files
```

## Quick Start

1. Install dependencies:
   ```bash
   pip install -r config/requirements.txt
   ```

2. Run the application:
   ```bash
   python app.py
   ```

3. Test the API:
   ```bash
   python scripts/test_api_tokens.py
   ```

## API Endpoints

- **Health Check**: `GET /health`
- **OTP**: `POST /api/otp/send`, `POST /calls/otp/verify`, `POST /calls/otp/replay`
- **Tokens**: `POST /api/tokens`, `GET /api/tokens`, `POST /api/tokens/validate`

## Testing

Run all tests:
```bash
pytest tests/
```

## Security Features

- Secure OTP generation
- API token authentication
- Input validation and sanitization
- Rate limiting ready
"""
    
    with open('docs/README.md', 'w') as f:
        f.write(readme_content)
    print("Created organized README.md")

def main():
    """Execute repository organization"""
    print("🧹 Starting repository organization...")
    print("=" * 50)
    
    try:
        create_directory_structure()
        organize_python_files()
        organize_config_files()
        organize_documentation()
        organize_test_files()
        clean_temporary_files()
        create_readme()
        
        print("=" * 50)
        print("✅ Repository organization complete!")
        print("\nYour repository is now clean and well-organized!")
        
    except Exception as e:
        print(f"❌ Error during organization: {e}")
        print("Please check file permissions and try again.")

if __name__ == "__main__":
    main()