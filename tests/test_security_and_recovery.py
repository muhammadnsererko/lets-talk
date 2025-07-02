import unittest
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from voice_api.plugins import analytics, tamper_detection, backup_manager
from voice_api.utils import security
import tempfile

class TestSecurityUtils(unittest.TestCase):
    def test_aes256_encrypt_decrypt(self):
        password = 'testpass123'
        plaintext = b'secret data!'
        ciphertext = security.encrypt_aes256(plaintext, password)
        decrypted = security.decrypt_aes256(ciphertext, password)
        self.assertEqual(decrypted, plaintext)
    def test_wrong_password(self):
        password = 'testpass123'
        plaintext = b'secret data!'
        ciphertext = security.encrypt_aes256(plaintext, password)
        with self.assertRaises(Exception):
            security.decrypt_aes256(ciphertext, 'wrongpass')
    def test_sha256_hash_file_and_bytes(self):
        with tempfile.NamedTemporaryFile(delete=False) as tf:
            tf.write(b'hello world')
            tf.flush()
            file_hash = security.sha256_hash_file(tf.name)
        bytes_hash = security.sha256_hash_bytes(b'hello world')
        self.assertEqual(file_hash, bytes_hash)
        os.unlink(tf.name)

class TestTamperDetection(unittest.TestCase):
    def setUp(self):
        self.module = tamper_detection.LocalTamperDetectionModule()
        # Create dummy critical files
        for f in tamper_detection.CRITICAL_FILES:
            with open(f, 'w') as fp:
                fp.write('test')
        self.module.update_hashes()
    def tearDown(self):
        for f in tamper_detection.CRITICAL_FILES:
            if os.path.exists(f):
                os.remove(f)
        if os.path.exists(tamper_detection.TAMPER_STATE_FILE):
            os.remove(tamper_detection.TAMPER_STATE_FILE)
    def test_integrity_ok(self):
        ok, msg = self.module.check_integrity()
        self.assertTrue(ok)
        self.assertEqual(msg, 'All files intact.')
    def test_integrity_tampered(self):
        # Modify a file
        with open(tamper_detection.CRITICAL_FILES[0], 'w') as fp:
            fp.write('tampered!')
        ok, msg = self.module.check_integrity()
        self.assertFalse(ok)
        self.assertIn('File tampered or reset', msg)

class TestBackupManager(unittest.TestCase):
    def setUp(self):
        self.module = backup_manager.LocalBackupManagerModule()
        self.user_id = 'user001'
        self.codes = ['123456', '654321']
        self.recovery_info = {'secret_answer': 'blue', 'passphrase': 'mysecret'}
        # Clean up files
        if os.path.exists(backup_manager.BACKUP_CODES_FILE):
            os.remove(backup_manager.BACKUP_CODES_FILE)
        if os.path.exists(backup_manager.RECOVERY_STATE_FILE):
            os.remove(backup_manager.RECOVERY_STATE_FILE)
        if os.path.exists(getattr(backup_manager, 'FERNET_KEYS_FILE', '')):
            os.remove(getattr(backup_manager, 'FERNET_KEYS_FILE', ''))
        # Ensure required files exist
        if not os.path.exists(backup_manager.BACKUP_CODES_FILE):
            with open(backup_manager.BACKUP_CODES_FILE, 'w') as f:
                f.write('')
        if not os.path.exists(backup_manager.RECOVERY_STATE_FILE):
            with open(backup_manager.RECOVERY_STATE_FILE, 'w') as f:
                f.write('{}')
        if hasattr(backup_manager, 'FERNET_KEYS_FILE') and not os.path.exists(backup_manager.FERNET_KEYS_FILE):
            with open(backup_manager.FERNET_KEYS_FILE, 'w') as f:
                f.write('{}')
    def tearDown(self):
        if os.path.exists(backup_manager.BACKUP_CODES_FILE):
            os.remove(backup_manager.BACKUP_CODES_FILE)
        if os.path.exists(backup_manager.RECOVERY_STATE_FILE):
            os.remove(backup_manager.RECOVERY_STATE_FILE)
        if os.path.exists(getattr(backup_manager, 'FERNET_KEYS_FILE', '')):
            os.remove(getattr(backup_manager, 'FERNET_KEYS_FILE', ''))
    def test_store_and_load_backup_codes(self):
        self.module.store_backup_codes(self.user_id, self.codes, password=None, recovery_info=self.recovery_info)
        loaded = self.module.load_backup_codes(self.user_id)
        self.assertEqual(loaded, self.codes)
    def test_wrong_password(self):
        self.module.store_backup_codes(self.user_id, self.codes, password=None, recovery_info=self.recovery_info)
        loaded = self.module.load_backup_codes(self.user_id, password='wrongpass')
        self.assertIsNone(loaded)
    def test_recover_backup_codes_secret(self):
        self.module.store_backup_codes(self.user_id, self.codes, password=None, recovery_info=self.recovery_info)
        rec_info = {'secret_answer': 'blue'}
        recovered = self.module.recover_backup_codes(self.user_id, rec_info)
        self.assertEqual(recovered, self.codes)
    def test_recover_backup_codes_fail(self):
        self.module.store_backup_codes(self.user_id, self.codes, password=None, recovery_info=self.recovery_info)
        rec_info = {'secret_answer': 'wrong'}
        recovered = self.module.recover_backup_codes(self.user_id, rec_info)
        self.assertIsNone(recovered)

class TestSecurityAndRecovery(unittest.TestCase):
    def run(self, result=None):
        try:
            super().run(result)
        except Exception as e:
            analytics.track_event('test_suite', 'test_failure', {'error': str(e), 'test': self.id()})
            raise
    def test_placeholder(self):
        self.assertTrue(True)

if __name__ == '__main__':
    unittest.main()