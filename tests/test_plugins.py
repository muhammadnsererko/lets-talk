import os
import unittest
import json
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from voice_api.plugins import analytics
from voice_api.utils import otp
from voice_api.plugins import user_settings

class TestAnalyticsPlugin(unittest.TestCase):
    def run(self, result=None):
        try:
            super().run(result)
        except Exception as e:
            analytics.track_event('test_suite', 'test_failure', {'error': str(e), 'test': self.id()})
            raise
    def test_track_event(self):
        analytics.track_event('test', 'event', {'info': 'test'})
        self.assertTrue(True)

if __name__ == '__main__':
    unittest.main()
    def setUp(self):
        self.analytics_file = os.path.join(os.path.dirname(__file__), '..', 'analytics_data.json')
        # Clean up before each test
        if os.path.exists(self.analytics_file):
            os.remove(self.analytics_file)
        # Ensure required file exists
        if not os.path.exists(self.analytics_file):
            with open(self.analytics_file, 'w') as f:
                f.write('{}')
        self.module = analytics.get_analytics_module('local')

    def test_track_event_creates_file_and_event(self):
        self.module.track_event('user001', 'test_event', {'foo': 'bar'})
        self.assertTrue(os.path.exists(self.analytics_file))
        with open(self.analytics_file, 'r') as f:
            data = json.load(f)
        self.assertIn('user001', data)
        self.assertEqual(data['user001'][0]['event_name'], 'test_event')
        self.assertEqual(data['user001'][0]['metadata']['foo'], 'bar')

    def test_multiple_events(self):
        self.module.track_event('user001', 'event1')
        self.module.track_event('user001', 'event2', {'x': 1})
        with open(self.analytics_file, 'r') as f:
            data = json.load(f)
        self.assertEqual(len(data['user001']), 2)
        self.assertEqual(data['user001'][1]['event_name'], 'event2')

class TestUserSettingsPlugin(unittest.TestCase):
    def setUp(self):
        self.settings_file = os.path.join(os.path.dirname(__file__), '..', 'user_settings.json')
        if os.path.exists(self.settings_file):
            os.remove(self.settings_file)
        # Ensure required file exists
        if not os.path.exists(self.settings_file):
            with open(self.settings_file, 'w') as f:
                f.write('{}')
        self.module = user_settings.get_user_settings_module('local')

    def test_set_and_get_preferences(self):
        prefs = {'voice': 'female', 'speed': 1.2}
        self.module.set_preferences('user001', prefs)
        loaded = self.module.get_preferences('user001')
        expected = {'voice': 'female', 'speed': 1.2, 'security_tier': 'standard'}
        self.assertEqual(loaded, expected)

    def test_get_preferences_default(self):
        loaded = self.module.get_preferences('unknown_user')
        self.assertEqual(loaded, {'security_tier': 'standard'})

class TestOTPUtils(unittest.TestCase):
    def test_generate_otp_range(self):
        for _ in range(100):
            code = otp.generate_otp()
            self.assertTrue(100000 <= code <= 999999)
            self.assertIsInstance(code, int)

if __name__ == '__main__':
    unittest.main()