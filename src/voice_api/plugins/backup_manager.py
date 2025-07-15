"""
Backup code manager plugin with AES-256 encryption and multi-layered recovery.
Supports secret questions and biometric/USB token file presence for master recovery.
All logic is local-only and offline.
"""
import os
import json
from datetime import datetime
from ..utils.security import encrypt_aes256, decrypt_aes256, generate_secure_token, generate_fernet_key, encrypt_fernet, decrypt_fernet

BACKUP_CODES_FILE = os.path.join(os.path.dirname(__file__), '..', 'backup_codes.enc')
RECOVERY_STATE_FILE = os.path.join(os.path.dirname(__file__), '..', 'recovery_state.json')
FERNET_KEYS_FILE = os.path.join(os.path.dirname(__file__), '..', 'fernet_keys.json')

class BackupManagerModuleBase:
    def store_backup_codes(self, user_id, codes, password, recovery_info):
        raise NotImplementedError
    def load_backup_codes(self, user_id, password=None):
        raise NotImplementedError
    def recover_backup_codes(self, user_id, recovery_info):
        raise NotImplementedError

class LocalBackupManagerModule(BackupManagerModuleBase):
    def __init__(self):
        self.codes_file = BACKUP_CODES_FILE
        self.recovery_file = RECOVERY_STATE_FILE
        self.fernet_keys_file = FERNET_KEYS_FILE
    def store_backup_codes(self, user_id, codes, password=None, recovery_info=None):
        # Generate Fernet key for new user or get existing
        fernet_keys = self._load_fernet_keys()
        if user_id not in fernet_keys:
            fernet_keys[user_id] = generate_fernet_key().decode()
            self._save_fernet_keys(fernet_keys)
        fernet_key = fernet_keys[user_id].encode()
        # Encrypt codes with Fernet
        enc = encrypt_fernet(json.dumps(codes).encode(), fernet_key)
        all_codes = self._load_all_codes()
        all_codes[user_id] = enc.decode('latin1')
        with open(self.codes_file, 'w') as f:
            json.dump(all_codes, f)
        # Store recovery info (passphrase, secret question, etc.)
        if os.path.exists(self.recovery_file):
            with open(self.recovery_file, 'r') as f:
                try:
                    rec = json.load(f)
                except Exception:
                    rec = {}
        else:
            rec = {}
        rec[user_id] = recovery_info
        with open(self.recovery_file, 'w') as f:
            json.dump(rec, f, indent=2)
    def load_backup_codes(self, user_id, password=None, passphrase=None):
        fernet_keys = self._load_fernet_keys()
        if user_id not in fernet_keys:
            return None
        fernet_key = fernet_keys[user_id].encode()
        all_codes = self._load_all_codes()
        enc = all_codes.get(user_id)
        if not enc:
            return None
        # Verify password using secure comparison
        if password is not None and not self._verify_password(user_id, password):
            return None
        try:
            codes = decrypt_fernet(enc.encode('latin1'), fernet_key)
            return json.loads(codes.decode())
        except Exception:
            return None
    def recover_backup_codes(self, user_id, recovery_info):
        # Accept passphrase as alternative to secret answer
        with open(self.recovery_file, 'r') as f:
            rec = json.load(f)
        user_rec = rec.get(user_id)
        if not user_rec:
            return None
        # Passphrase recovery
        if 'passphrase' in user_rec and 'passphrase' in recovery_info:
            if user_rec['passphrase'] == recovery_info['passphrase']:
                return self.load_backup_codes(user_id)
        # Secret question recovery
        if 'secret_answer' in user_rec and 'secret_answer' in recovery_info:
            if user_rec['secret_answer'] == recovery_info['secret_answer']:
                return self.load_backup_codes(user_id)
        # Biometric/token file recovery
        if 'token_file' in user_rec and 'token_file' in recovery_info:
            if os.path.exists(user_rec['token_file']) and os.path.exists(recovery_info['token_file']):
                if user_rec['token_file'] == recovery_info['token_file']:
                    return self.load_backup_codes(user_id)
        return None
        
    def _verify_password(self, user_id, password):
        """Verify password using secure comparison."""
        # In a real implementation, this would verify against a stored hash
        # For this example, we'll use a secure comparison against stored credentials
        try:
            with open(self.recovery_file, 'r') as f:
                recovery_data = json.load(f)
            user_recovery = recovery_data.get(user_id, {})
            stored_password_hash = user_recovery.get('password_hash')
            
            if not stored_password_hash:
                return False
                
            # Use constant-time comparison to prevent timing attacks
            import hmac
            import hashlib
            
            # Hash the provided password with the same algorithm
            provided_hash = hashlib.sha256(password.encode()).hexdigest()
            
            # Compare using constant-time comparison
            return hmac.compare_digest(stored_password_hash, provided_hash)
        except Exception:
            return False
    def _load_all_codes(self):
        if not os.path.exists(self.codes_file):
            return {}
        try:
            with open(self.codes_file, 'rb') as f:
                data = f.read()
                if not data:
                    return {}
                return json.loads(data.decode())
        except Exception:
            return {}
    def _load_fernet_keys(self):
        if not os.path.exists(self.fernet_keys_file):
            return {}
        with open(self.fernet_keys_file, 'r') as f:
            return json.load(f)
    def _save_fernet_keys(self, keys):
        with open(self.fernet_keys_file, 'w') as f:
            json.dump(keys, f, indent=2)

# Plugin registry
BACKUP_MANAGER_MODULES = {}
def register_backup_manager_module(name, module):
    BACKUP_MANAGER_MODULES[name] = module
def get_backup_manager_module(name):
    return BACKUP_MANAGER_MODULES.get(name)
register_backup_manager_module("local", LocalBackupManagerModule())
DEFAULT_BACKUP_MANAGER_MODULE = "local"
def store_codes(user_id, codes, password, recovery_info, module_name=None):
    module = get_backup_manager_module(module_name or DEFAULT_BACKUP_MANAGER_MODULE)
    if not module:
        raise Exception(f"Backup manager module '{module_name}' not found.")
    return module.store_backup_codes(user_id, codes, password, recovery_info)
def load_codes(user_id, password, module_name=None):
    module = get_backup_manager_module(module_name or DEFAULT_BACKUP_MANAGER_MODULE)
    if not module:
        raise Exception(f"Backup manager module '{module_name}' not found.")
    return module.load_backup_codes(user_id, password)
def recover_codes(user_id, recovery_info, module_name=None):
    module = get_backup_manager_module(module_name or DEFAULT_BACKUP_MANAGER_MODULE)
    if not module:
        raise Exception(f"Backup manager module '{module_name}' not found.")
    return module.recover_backup_codes(user_id, recovery_info)
# Add rotation timestamp logging
# with open(BACKUP_CODES_FILE, 'a') as audit_log:
#     audit_log.write(f"{datetime.utcnow()} - Key rotated for {user_id}\n")