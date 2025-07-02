import unittest
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from voice_api.plugins import analytics
from voice_api.utils.learning_module import LearningModule

class TestLearningModule(unittest.TestCase):
    def run(self, result=None):
        try:
            super().run(result)
        except Exception as e:
            analytics.track_event('test_suite', 'test_failure', {'error': str(e), 'test': self.id()})
            raise
    def test_pattern_detection(self):
        module = LearningModule()
        module.observe('user', 'fail')
        module.observe('user', 'fail')
        module.observe('user', 'success')
        pattern = module.detect_pattern('user')
        self.assertIn('fail', pattern)

if __name__ == '__main__':
    unittest.main()