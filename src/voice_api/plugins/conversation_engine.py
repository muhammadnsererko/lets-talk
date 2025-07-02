"""
Modular conversation engine for smart voice interaction and adaptive learning.
Handles simple spoken interactions and adapts responses based on local analytics and user preferences.
"""
import random
from voice_api.plugins import analytics, user_settings

class ConversationEngineBase:
    def get_response(self, user_id, context):
        raise NotImplementedError("Conversation engines must implement get_response.")

class SimpleAdaptiveConversationEngine(ConversationEngineBase):
    def __init__(self):
        self.default_prompts = [
            "Would you like me to repeat that code?",
            "Do you want to hear the OTP again?",
            "Should I slow down the next time?"
        ]
    def get_response(self, user_id, context):
        # Analyze analytics for replay frequency
        replay_count = self._get_replay_count(user_id)
        prefs = user_settings.get_user_preferences(user_id)
        # Adapt prompt based on replay frequency and preferences
        if replay_count > 2:
            return "I noticed you replayed the code several times. Would you like me to slow down or change the voice?"
        if prefs.get("voice") == "male":
            return "Would you like to switch to a different voice or adjust the speed?"
        return random.choice(self.default_prompts)
    def _get_replay_count(self, user_id):
        # Count replay events from analytics
        try:
            module = analytics.get_analytics_module("local")
            with open(module.analytics_file, 'r') as f:
                data = f.read()
            import json
            events = json.loads(data).get(user_id, [])
            return sum(1 for e in events if e["event_name"] == "otp_replay")
        except Exception:
            return 0

# Plugin registry for conversation engines
CONVERSATION_ENGINES = {}

def register_conversation_engine(name, engine):
    CONVERSATION_ENGINES[name] = engine

def get_conversation_engine(name):
    return CONVERSATION_ENGINES.get(name)

# Register the default engine
register_conversation_engine("simple_adaptive", SimpleAdaptiveConversationEngine())

def get_conversation_response(user_id, context, engine_name=None):
    engine = get_conversation_engine(engine_name or "simple_adaptive")
    if not engine:
        raise Exception(f"Conversation engine '{engine_name}' not found.")
    return engine.get_response(user_id, context)