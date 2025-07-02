"""
Local learning plugin for adaptive OTP voice delivery.
Tracks user behavior, detects patterns, and dynamically adjusts user settings.
All logic and data are local-only and privacy-safe.
"""
import os
import json
import threading
from voice_api.plugins import user_settings

LEARNING_FILE = os.path.join(os.path.dirname(__file__), '..', 'learning_data.json')

class LearningModuleBase:
    def track_behavior(self, user_id, event_name, metadata=None):
        raise NotImplementedError
    def analyze_patterns(self, user_id):
        raise NotImplementedError
    def reset_learning(self, user_id=None):
        raise NotImplementedError
    def get_learning_data(self, user_id=None):
        raise NotImplementedError

class LocalLearningModule(LearningModuleBase):
    def __init__(self):
        self.learning_file = LEARNING_FILE
        self.lock = threading.Lock()
        if not os.path.exists(self.learning_file):
            with open(self.learning_file, 'w') as f:
                json.dump({}, f)
    def _load(self):
        with self.lock:
            try:
                with open(self.learning_file, 'r') as f:
                    return json.load(f)
            except Exception:
                return {}
    def _save(self, data):
        with self.lock:
            with open(self.learning_file, 'w') as f:
                json.dump(data, f, indent=2)
    def track_behavior(self, user_id, event_name, metadata=None):
        data = self._load()
        if user_id not in data:
            data[user_id] = {
                'otp_replay': 0,
                'otp_success': 0,
                'otp_failure': 0,
                'speech_rate_changes': 0,
                'volume_changes': 0,
                'last_events': []
            }
        if event_name == 'otp_replay':
            data[user_id]['otp_replay'] += 1
        elif event_name == 'otp_success':
            data[user_id]['otp_success'] += 1
        elif event_name == 'otp_failure':
            data[user_id]['otp_failure'] += 1
        elif event_name == 'speech_rate_change':
            data[user_id]['speech_rate_changes'] += 1
        elif event_name == 'volume_change':
            data[user_id]['volume_changes'] += 1
        # Track last 10 events
        ev = {'event': event_name, 'metadata': metadata or {}}
        data[user_id]['last_events'].append(ev)
        data[user_id]['last_events'] = data[user_id]['last_events'][-10:]
        self._save(data)
        self.analyze_patterns(user_id)
    def analyze_patterns(self, user_id):
        data = self._load()
        user = data.get(user_id, {})
        # Rule-based: If user replays OTP >3 times, slow down speech
        if user.get('otp_replay', 0) >= 3:
            prefs = user_settings.get_user_preferences(user_id)
            if prefs.get('speed', 1.0) >= 1.0:
                prefs['speed'] = 0.8
                user_settings.set_user_preferences(user_id, prefs)
        # If user changes volume >2 times, set volume to preferred
        if user.get('volume_changes', 0) >= 2:
            prefs = user_settings.get_user_preferences(user_id)
            if prefs.get('volume', 1.0) != 1.2:
                prefs['volume'] = 1.2
                user_settings.set_user_preferences(user_id, prefs)
        # If user fails OTP >2 times, suggest language change
        if user.get('otp_failure', 0) >= 2:
            prefs = user_settings.get_user_preferences(user_id)
            if prefs.get('language', 'en') == 'en':
                prefs['language'] = 'es'
                user_settings.set_user_preferences(user_id, prefs)
    def reset_learning(self, user_id=None):
        if user_id is None:
            self._save({})
        else:
            data = self._load()
            if user_id in data:
                del data[user_id]
            self._save(data)
    def get_learning_data(self, user_id=None):
        data = self._load()
        if user_id:
            return data.get(user_id, {})
        return data

# Plugin registry
LEARNING_MODULES = {}
def register_learning_module(name, module):
    LEARNING_MODULES[name] = module
def get_learning_module(name):
    return LEARNING_MODULES.get(name)
register_learning_module("local", LocalLearningModule())
DEFAULT_LEARNING_MODULE = "local"
def track_behavior(user_id, event_name, metadata=None, module_name=None):
    module = get_learning_module(module_name or DEFAULT_LEARNING_MODULE)
    if not module:
        raise Exception(f"Learning module '{module_name}' not found.")
    module.track_behavior(user_id, event_name, metadata)
def reset_learning(user_id=None, module_name=None):
    module = get_learning_module(module_name or DEFAULT_LEARNING_MODULE)
    if not module:
        raise Exception(f"Learning module '{module_name}' not found.")
    module.reset_learning(user_id)
def get_learning_data(user_id=None, module_name=None):
    module = get_learning_module(module_name or DEFAULT_LEARNING_MODULE)
    if not module:
        raise Exception(f"Learning module '{module_name}' not found.")
    return module.get_learning_data(user_id)