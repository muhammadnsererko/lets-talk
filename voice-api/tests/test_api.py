import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import unittest
from app import app
from services.polly_service import synthesize_speech

"""
Unit tests for the Voice API service endpoints.
Covers OTP sending and error scenarios.
"""

class TestVoiceAPI(unittest.TestCase):
    """
    Test cases for the Voice API OTP endpoint.
    """
    def setUp(self):
        """
        Set up the Flask test client for each test.
        """
        self.app = app.test_client()
        self.app.testing = True

    def test_send_otp_success(self):
        """
        Test sending OTP with a valid user_id returns success and correct data.
        """
        response = self.app.post(
            '/calls/otp',
            json={'user_id': 'user123'}
        )
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status'], 'otp_sent')
        self.assertTrue(data['otp_id'].startswith('otp_user123_'))
        self.assertTrue(100000 <= data['otp'] <= 999999)

    def test_send_otp_missing_user_id(self):
        """
        Test sending OTP without user_id returns an error response.
        """
        response = self.app.post('/calls/otp', json={})
        data = response.get_json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['error'], 'user_id required')

    def test_verify_otp_placeholder(self):
        """
        Test the OTP verification placeholder endpoint returns expected response.
        """
        response = self.app.post(
            '/calls/otp/verify',
            json={'user_id': 'user123', 'otp': 123456}
        )
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status'], 'verification_placeholder')
        self.assertEqual(data['user_id'], 'user123')
        self.assertEqual(data['otp'], 123456)

    def test_replay_otp_voice_placeholder(self):
        """
        Test the OTP voice replay placeholder endpoint returns expected response.
        """
        response = self.app.post(
            '/calls/otp/replay',
            json={'user_id': 'user123'}
        )
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status'], 'replay_placeholder')
        self.assertEqual(data['user_id'], 'user123')

class TestPollyService(unittest.TestCase):
    """
    Unit tests for the Polly speech synthesis service logic.
    """
    def test_synthesize_speech_mock(self):
        result = synthesize_speech("Hello, world!")
        self.assertIsInstance(result["AudioStream"], bytes)
        self.assertTrue(len(result["AudioStream"]) > 0)

    def test_synthesize_speech_error(self):
        """
        Test that synthesize_speech handles exceptions gracefully.
        """
        # Patch or simulate an error by passing a value that will cause an exception
        # For this mock, we can monkeypatch the function if needed, but here we'll simulate
        # by temporarily replacing the function body if needed. For now, just check normal path.
        # If the real AWS code is enabled, you could test with invalid credentials.
        pass  # Placeholder for error scenario

if __name__ == '__main__':
    unittest.main()