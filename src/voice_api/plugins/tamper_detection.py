"""
Tamper-detection plugin for monitoring file integrity using SHA-256 hashes.
Blocks or warns if critical files are altered. All logic is local-only.
"""
import os
import json
import hashlib
from voice_api.utils.security import sha256_hash_file

TAMPER_STATE_FILE = os.path.join(os.path.dirname(__file__), '..', 'tamper_state.json')

CRITICAL_FILES = [
    os.path.join(os.path.dirname(__file__), '..', 'backup_codes.enc'),
    os.path.join(os.path.dirname(__file__), '..', 'user_settings.enc'),
    os.path.join(os.path.dirname(__file__), '..', 'fernet_keys.json'),
    os.path.join(os.path.dirname(__file__), '..', 'learning_data.json'),
]

class TamperDetectionModuleBase:
    def check_integrity(self):
        raise NotImplementedError
    def update_hashes(self):
        raise NotImplementedError

class LocalTamperDetectionModule(TamperDetectionModuleBase):
    def __init__(self):
        self.state_file = TAMPER_STATE_FILE
        self.critical_files = CRITICAL_FILES
        if not os.path.exists(self.state_file):
            self.update_hashes()
    def check_integrity(self):
        if not os.path.exists(self.state_file):
            return False, 'Tamper state file missing.'
        with open(self.state_file, 'r') as f:
            baseline = json.load(f)
        for file in self.critical_files:
            if not os.path.exists(file):
                return False, f'Critical file missing: {file}'
            try:
                with open(file, 'rb') as cf:
                    data = cf.read()
                    file_hash = hashlib.sha256(data).hexdigest()
                if file not in baseline or baseline[file] != file_hash:
                    return False, f'File tampered or reset: {file}'
            except Exception:
                return False, f'File unreadable or corrupted: {file}'
        return True, 'All files intact.'
    def update_hashes(self):
        baseline = {}
        for file in self.critical_files:
            if os.path.exists(file):
                with open(file, 'rb') as cf:
                    data = cf.read()
                    baseline[file] = hashlib.sha256(data).hexdigest()
        with open(self.state_file, 'w') as f:
            json.dump(baseline, f, indent=2)

# Plugin registry
TAMPER_MODULES = {}
def register_tamper_module(name, module):
    TAMPER_MODULES[name] = module
def get_tamper_module(name):
    return TAMPER_MODULES.get(name)
register_tamper_module("local", LocalTamperDetectionModule())
DEFAULT_TAMPER_MODULE = "local"
def check_tamper(module_name=None):
    module = get_tamper_module(module_name or DEFAULT_TAMPER_MODULE)
    if not module:
        raise Exception(f"Tamper module '{module_name}' not found.")
    return module.check_integrity()
def update_tamper_hashes(module_name=None):
    module = get_tamper_module(module_name or DEFAULT_TAMPER_MODULE)
    if not module:
        raise Exception(f"Tamper module '{module_name}' not found.")
    return module.update_hashes()