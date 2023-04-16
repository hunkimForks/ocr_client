import base64
import os
import unittest
from upstage.api import Extractor


UPSTAGE_API_EXTRACTOR_URL = os.environ["UPSTAGE_API_EXTRACTOR_URL"]
UPSTAGE_API_KEY = os.environ["UPSTAGE_API_KEY"]


class TestExtractor(unittest.TestCase):
    def setUp(self):
        self.client = Extractor(UPSTAGE_API_EXTRACTOR_URL, UPSTAGE_API_KEY, timeout=30, log_level="INFO")
        self.filename = os.path.join(os.path.dirname(__file__), "data", "receipt.jpg")

    def test_request_with_filename(self):
        result = self.client.request(self.filename)
        self.assertIsInstance(result, dict)

    def test_request_with_byte_string(self):
        with open(self.filename, "rb") as f:
            image_bytes = f.read()
        result = self.client.request(image_bytes)
        self.assertIsInstance(result, dict)

    def test_request_with_base64_string(self):
        with open(self.filename, "rb") as f:
            image_bytes = f.read()
        image_base64 = base64.b64encode(image_bytes).decode("utf-8")
        result = self.client.request(image_base64)
        self.assertIsInstance(result, dict)


class TestExtractorRedaction(unittest.TestCase):
    def setUp(self):
        self.client = Extractor(UPSTAGE_API_EXTRACTOR_URL, UPSTAGE_API_KEY, redact=True, timeout=30, log_level="INFO")
        self.filename = os.path.join(os.path.dirname(__file__), "data", "receipt.jpg")

    def test_request_with_filename(self):
        result = self.client.request(self.filename)
        self.assertTrue(result.get("redacted"))


if __name__ == "__main__":
    unittest.main()
