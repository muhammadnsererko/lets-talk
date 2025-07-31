import os
import json
import datetime

ANALYTICS_FILE = 'analytics_data.json'

class AnalyticsModuleBase:
    def track_event(self, user_id, event_name, metadata=None):
        raise NotImplementedError("Analytics modules must implement the track_event method.")

class LocalAnalyticsModule(AnalyticsModuleBase):
    def __init__(self):
        self.analytics_file = ANALYTICS_FILE
        if not os.path.exists(self.analytics_file):
            with open(self.analytics_file, 'w') as f:
                json.dump({}, f)

    def track_event(self, user_id, event_name, metadata=None):
        with open(self.analytics_file, 'r+') as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = {}
            if user_id not in data:
                data[user_id] = []
            event = {
                "event_name": event_name,
                "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
                "metadata": metadata or {}
            }
            data[user_id].append(event)
            f.seek(0)
            json.dump(data, f, indent=2)
            f.truncate()

# Plugin registry for analytics modules
ANALYTICS_MODULES = {}

def register_analytics_module(name, module):
    ANALYTICS_MODULES[name] = module

def get_analytics_module(name):
    return ANALYTICS_MODULES.get(name)

# Register the default local analytics module
register_analytics_module("local", LocalAnalyticsModule())

# Default track_event function using the selected analytics module
DEFAULT_ANALYTICS_MODULE = "local"

def track_event(user_id, event_name, metadata=None, module_name=None):
    module = get_analytics_module(module_name or DEFAULT_ANALYTICS_MODULE)
    if not module:
        raise Exception(f"Analytics module '{module_name}' not found.")
    module.track_event(user_id, event_name, metadata)