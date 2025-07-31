"""
User settings plugin for customizing voice, delivery preferences, and security tiers.
All settings are stored locally for privacy and offline support.
"""
import os
import json

SETTINGS_FILE = 'user_settings.json'

SECURITY_TIERS = ["paranoid", "strict", "standard"]

class UserSettingsModuleBase:
    def set_preferences(self, user_id, preferences):
        raise NotImplementedError("User settings modules must implement set_preferences.")
    def get_preferences(self, user_id):
        raise NotImplementedError("User settings modules must implement get_preferences.")

from voice_api.utils.security import generate_fernet_key, encrypt_fernet, decrypt_fernet
import os

USER_SETTINGS_FILE = os.path.join(os.path.dirname(__file__), '..', 'user_settings.enc')
FERNET_KEYS_FILE = os.path.join(os.path.dirname(__file__), '..', 'fernet_keys.json')

class LocalUserSettingsModule(UserSettingsModuleBase):
    def __init__(self):
        self.settings_file = USER_SETTINGS_FILE
        self.fernet_keys_file = FERNET_KEYS_FILE
        if not os.path.exists(self.settings_file):
            with open(self.settings_file, 'wb') as f:
                f.write(b'')
        if not os.path.exists(self.fernet_keys_file):
            with open(self.fernet_keys_file, 'w') as f:
                json.dump({}, f)
    def set_user_settings(self, user_id, settings):
        fernet_keys = self._load_fernet_keys()
        if user_id not in fernet_keys:
            fernet_keys[user_id] = generate_fernet_key().decode()
            self._save_fernet_keys(fernet_keys)
        fernet_key = fernet_keys[user_id].encode()
        enc = encrypt_fernet(json.dumps(settings).encode(), fernet_key)
        all_settings = self._load_all_settings()
        all_settings[user_id] = enc.decode('latin1')
        with open(self.settings_file, 'wb') as f:
            json.dump(all_settings, f)
    def get_user_settings(self, user_id):
        fernet_keys = self._load_fernet_keys()
        if user_id not in fernet_keys:
            return None
        fernet_key = fernet_keys[user_id].encode()
        all_settings = self._load_all_settings()
        enc = all_settings.get(user_id)
        if not enc:
            return None
        try:
            settings = decrypt_fernet(enc.encode('latin1'), fernet_key)
            return json.loads(settings.decode())
        except Exception:
            return None
    def _load_all_settings(self):
        if not os.path.exists(self.settings_file):
            return {}
        try:
            with open(self.settings_file, 'rb') as f:
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
    def set_preferences(self, user_id, preferences):
        # Ensure security_tier is valid if provided
        if "security_tier" in preferences:
            if preferences["security_tier"] not in SECURITY_TIERS:
                raise ValueError(f"Invalid security_tier: {preferences['security_tier']}")
        data = {}
        if os.path.exists(self.settings_file):
            try:
                with open(self.settings_file, 'r') as f:
                    content = f.read().strip()
                    if content:
                        data = json.loads(content)
            except Exception:
                data = {}
        data[user_id] = preferences
        with open(self.settings_file, 'w') as f:
            json.dump(data, f, indent=2)
    def get_preferences(self, user_id):
        data = {}
        if os.path.exists(self.settings_file):
            try:
                with open(self.settings_file, 'r') as f:
                    content = f.read().strip()
                    if content:
                        data = json.loads(content)
            except Exception:
                data = {}
        prefs = data.get(user_id, {})
        # Default to 'standard' if not set
        if "security_tier" not in prefs:
            prefs["security_tier"] = "standard"
        return prefs

# Plugin registry for user settings modules
USER_SETTINGS_MODULES = {}

def register_user_settings_module(name, module):
    USER_SETTINGS_MODULES[name] = module

def get_user_settings_module(name):
    return USER_SETTINGS_MODULES.get(name)

# Register the default local user settings module
register_user_settings_module("local", LocalUserSettingsModule())

# Default interface functions
DEFAULT_USER_SETTINGS_MODULE = "local"

def set_user_preferences(user_id, preferences, module_name=None):
    module = get_user_settings_module(module_name or DEFAULT_USER_SETTINGS_MODULE)
    if not module:
        raise Exception(f"User settings module '{module_name}' not found.")
    module.set_preferences(user_id, preferences)

def get_user_preferences(user_id, module_name=None):
    module = get_user_settings_module(module_name or DEFAULT_USER_SETTINGS_MODULE)
    if not module:
        raise Exception(f"User settings module '{module_name}' not found.")
    return module.get_preferences(user_id)