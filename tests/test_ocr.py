import base64
import os
import unittest
from upstage.api import OCR

UPSTAGE_API_OCR_URL = os.environ["OCR_BACKEND_URL"]
UPSTAGE_API_KEY = os.environ["OCR_SECRET"]


class TestOCR(unittest.TestCase):
    def setUp(self):
        # Set up OCR client
        self.client = OCR(UPSTAGE_API_OCR_URL, UPSTAGE_API_KEY, timeout=10, log_level="INFO")
        self.filename = os.path.join(os.path.dirname(__file__), "data", "upstage.png")

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


class TestOCRRedaction(unittest.TestCase):
    def setUp(self):
        self.client = OCR(UPSTAGE_API_OCR_URL, UPSTAGE_API_KEY, redact=True, timeout=10, log_level="INFO")
        self.filename = os.path.join(os.path.dirname(__file__), "data", "upstage.png")

    def test_request_with_filename(self):
        result = self.client.request(self.filename)
        self.assertTrue(result.get("redacted"))


if __name__ == "__main__":
    unittest.main()
