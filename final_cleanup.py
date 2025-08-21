#!/usr/bin/env python3
"""
Final cleanup script for voice-api repository
"""
import os
import shutil
import glob

def main():
    print("🔧 Final repository cleanup...")
    
    # Clean up any remaining temporary files
    temp_patterns = [
        '*.pyc',
        '__pycache__',
        '*.log',
        '*.tmp'
    ]
    
    for pattern in temp_patterns:
        for file in glob.glob(f'**/{pattern}', recursive=True):
            try:
                if os.path.isfile(file):
                    os.remove(file)
                    print(f"Cleaned: {file}")
                elif os.path.isdir(file):
                    shutil.rmtree(file)
                    print(f"Cleaned directory: {file}")
            except:
                pass
    
    # Ensure clean directory structure
    essential_dirs = ['tests', 'blueprints', 'docs']
    for dir_name in essential_dirs:
        os.makedirs(dir_name, exist_ok=True)
    
    print("✅ Repository cleanup complete!")
    print("\nYour repository is now clean and organized.")

if __name__ == "__main__":
    main()