import unittest
import numpy as np

from detection.preprocessor import preprocess_input
from app.services.detection_service import DetectionService


class TestDetector(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """
        Initialize detector once
        """
        cls.detector = DetectionService()

        # Sample valid input (matches feature structure)
        cls.sample_event = {
            "duration": 1,
            "protocol_type": "tcp",
            "service": "http",
            "flag": "SF",
            "src_bytes": 200,
            "dst_bytes": 1000,
            "wrong_fragment": 0,
            "urgent": 0,
            "hot": 0,
            "num_failed_logins": 0,
            "logged_in": 1,
            "num_compromised": 0,
            "root_shell": 0,
            "su_attempted": 0,
            "num_root": 0,
            "num_file_creations": 0,
            "num_shells": 0,
            "num_access_files": 0,
            "num_outbound_cmds": 0,
            "is_host_login": 0,
            "is_guest_login": 0,
            "count": 5,
            "srv_count": 5,
            "serror_rate": 0.0,
            "srv_serror_rate": 0.0,
            "rerror_rate": 0.0,
            "srv_rerror_rate": 0.0,
            "same_srv_rate": 1.0,
            "diff_srv_rate": 0.0,
            "srv_diff_host_rate": 0.0
        }
      
    # TEST PREPROCESSING

    def test_preprocess_input(self):
        processed = preprocess_input(self.sample_event)

        self.assertIsInstance(processed, (list, np.ndarray))
        self.assertTrue(len(processed) > 0)

    # TEST PREDICTION

    def test_prediction(self):
        result = self.detector.predict(self.sample_event)

        self.assertIsInstance(result, dict)
        self.assertIn("attack_type", result)
        self.assertIn("confidence", result)

    # TEST NORMAL TRAFFIC

    def test_normal_prediction(self):
        result = self.detector.predict(self.sample_event)

        self.assertIsInstance(result["attack_type"], str)

    # TEST INVALID INPUT

    def test_invalid_input(self):
        bad_event = {"invalid": "data"}

        result = self.detector.predict(bad_event)

        self.assertIsInstance(result, dict)
        self.assertTrue("error" in result or "attack_type" in result)

    # TEST EDGE VALUES

    def test_edge_values(self):
        edge_event = self.sample_event.copy()
        edge_event["src_bytes"] = 9999999
        edge_event["dst_bytes"] = 9999999

        result = self.detector.predict(edge_event)

        self.assertIsInstance(result, dict)
        self.assertIn("attack_type", result)


# RUN TESTS

if __name__ == "__main__":
    unittest.main()
