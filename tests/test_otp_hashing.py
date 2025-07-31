import unittest
import os
import json
from unittest.mock import patch
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from voice_api.utils.otp_logic import store_otp, get_stored_otp, OTP_STORE_FILE
from voice_api.utils.custom_exceptions import OTPStorageError

class TestOTPHashing(unittest.TestCase):

    def setUp(self):
        # Ensure the OTP store file is clean before each test
        if os.path.exists(OTP_STORE_FILE):
            os.remove(OTP_STORE_FILE)
        with open(OTP_STORE_FILE, 'w') as f:
            json.dump({}, f)

    def tearDown(self):
        # Clean up the OTP store file after each test
        if os.path.exists(OTP_STORE_FILE):
            os.remove(OTP_STORE_FILE)

    def test_store_otp_hashes_password(self):
        user_id = "test_user"
        otp = "123456"
        store_otp(user_id, otp)
        
        with open(OTP_STORE_FILE, 'r') as f:
            data = json.load(f)
            
        self.assertIn(user_id, data)
        self.assertNotEqual(otp, data[user_id]['otp'])
        self.assertTrue(len(data[user_id]['otp']) > len(otp))

    def test_get_stored_otp_verifies_correct_password(self):
        user_id = "test_user"
        otp = "123456"
        store_otp(user_id, otp)
        
        retrieved_otp = get_stored_otp(user_id, otp)
        self.assertIsNotNone(retrieved_otp)

    def test_get_stored_otp_rejects_incorrect_password(self):
        user_id = "test_user"
        otp = "123456"
        incorrect_otp = "654321"
        store_otp(user_id, otp)
        
        retrieved_otp = get_stored_otp(user_id, incorrect_otp)
        self.assertIsNone(retrieved_otp)

    @patch('builtins.open', side_effect=IOError("File not found"))
    def test_store_otp_raises_exception_on_file_error(self, mock_open):
        with self.assertRaises(OTPStorageError):
            store_otp("test_user", "123456")

if __name__ == '__main__':
    unittest.main()