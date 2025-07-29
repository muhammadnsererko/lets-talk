import unittest
import os
import sys
from datetime import datetime
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import app
from src.voice_api.plugins import analytics

class TestVoiceAPI(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        self.analytics_file = os.path.join(os.path.dirname(__file__), '..', 'src', 'voice_api', 'analytics_data.json')
        if os.path.exists(self.analytics_file):
            os.remove(self.analytics_file)
        if not os.path.exists(self.analytics_file):
            with open(self.analytics_file, 'w') as f:
                f.write('{}')
    def run(self, result=None):
        try:
            super().run(result)
        except Exception as e:
            analytics.track_event('test_suite', 'test_failure', {'error': str(e), 'test': self.id()})
            raise
    def test_send_and_verify_otp_real_flow(self):
        user_id = 'test_user123'
        
        # Test send OTP
        send_resp = self.client.post('/api/otp/send', json={'user_id': user_id})
        self.assertEqual(send_resp.status_code, 200)
        data = send_resp.get_json()
        self.assertIn('status', data)
        self.assertEqual(data['status'], 'success')
        self.assertIn('otp', data)
        
        otp_code = data['otp']
        
        # Test verify OTP
        verify_resp = self.client.post('/calls/otp/verify', json={
            'user_id': user_id, 
            'otp': otp_code
        })
        self.assertEqual(verify_resp.status_code, 200)
        verify_data = verify_resp.get_json()
        self.assertEqual(verify_data['status'], 'success')

    def test_send_otp_missing_user_id(self):
        resp = self.client.post('/api/otp/send', json={})
        self.assertEqual(resp.status_code, 400)

    def test_replay_otp_voice_placeholder(self):
        user_id = 'user123'
        resp = self.client.post('/calls/otp/replay', json={'user_id': user_id})
        self.assertIn(resp.status_code, [200, 404])

class TestPollyService(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
    def run(self, result=None):
        try:
            super().run(result)
        except Exception as e:
            analytics.track_event('test_suite', 'test_failure', {'error': str(e), 'test': self.id()})
            raise
    def test_synthesize_speech_mock(self):
        payload = {'text': 'Hello world', 'voice': 'Joanna'}
        resp = self.client.post('/api/polly/synthesize', json=payload)
        self.assertEqual(resp.status_code, 404)  # Endpoint removed

if __name__ == '__main__':
    unittest.main()
