import unittest
import os
import json

class BaseTestCase(unittest.TestCase):
    def create_test_file(self, file_path, initial_data=None):
        """
        Creates a test file with initial data.
        """
        if os.path.exists(file_path):
            os.remove(file_path)
        
        with open(file_path, 'w') as f:
            if initial_data is not None:
                json.dump(initial_data, f)
            else:
                f.write('{}')

    def tearDown(self):
        """
        Clean up any files created during tests.
        """
        if hasattr(self, 'analytics_file') and os.path.exists(self.analytics_file):
            os.remove(self.analytics_file)
        
        if hasattr(self, 'settings_file') and os.path.exists(self.settings_file):
            os.remove(self.settings_file)