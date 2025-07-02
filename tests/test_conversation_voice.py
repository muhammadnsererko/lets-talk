import unittest
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from voice_api.plugins import analytics
from voice_api.utils.conversation_engine import ConversationEngine
from voice_api.utils.ssml_voice_module import SSMLVoiceModule

class TestConversationEngine(unittest.TestCase):
    def run(self, result=None):
        try:
            super().run(result)
        except Exception as e:
            analytics.track_event('test_suite', 'test_failure', {'error': str(e), 'test': self.id()})
            raise
    def test_generate_response(self):
        engine = ConversationEngine()
        response = engine.generate_response('Hello')
        self.assertIsInstance(response, str)
        self.assertGreater(len(response), 0)

class TestSSMLVoiceModule(unittest.TestCase):
    def run(self, result=None):
        try:
            super().run(result)
        except Exception as e:
            analytics.track_event('test_suite', 'test_failure', {'error': str(e), 'test': self.id()})
            raise
    def test_synthesize_ssml(self):
        ssml_module = SSMLVoiceModule()
        ssml = '<speak>Hello world</speak>'
        audio = ssml_module.synthesize_ssml(ssml)
        self.assertIsNotNone(audio)

if __name__ == '__main__':
    unittest.main()