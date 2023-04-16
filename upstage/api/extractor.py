import base64
import logging
import os
import requests


def _process_image(image):
    # If input is a byte string, return as-is
    if isinstance(image, bytes):
        return image

    # If input is a filename, read
    elif isinstance(image, str) and os.path.isfile(image):
        return open(image, "rb").read()

    # Check if input is a base64 string, convert to bytes
    else:
        try:
            return base64.b64decode(image.split(",")[-1])
        except Exception as e:
            raise ValueError(f"Invalid input: image must be a filename, byte string, or base64 string: {e}")


class Extractor:
    def __init__(self, url: str, api_key: str, redact=False, timeout=10, log_level="INFO"):
        """
        Initializes an instance of the Extractor class.

        Args:
            url (str): The URL of the Extractor API endpoint.
            api_key (str): The API key used to authenticate with the Extractor API.
            redact (bool, optional): Whether to redact sensitive information from the result. Default is False.
            timeout (int, optional): The number of seconds to wait for a response from the Extractor API (default is 10).
            log_level (str, optional): The logging level for the Extractor instance (default is "INFO").

        Returns:
            None
        """
        # Set variables
        self.url = url
        self.api_key = api_key
        self.headers = {"Authorization": f"Bearer {self.api_key}"}
        self.payload = {"redact": redact}
        self.timeout = timeout
        self.log_level = log_level

        # Set logger
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(level=self.log_level)

    def request(self, image, confidence_threshold=0):
        """
        Requests Upstage Extractor API on the input image and returns the result as a dictionary.

        Args:
            image (str or bytes): The input image as a filename or byte string, or a base64-encoded string.
            confidence_threshold (float, optional): The minimum confidence score required for the Extractor result to be considered valid. Must be a value between 0 and 1. Default is 0.95.

        Returns:
            dict: The Extractor result as a dictionary.
        """
        # Process image
        files = {"image": _process_image(image)}

        # Get response
        response = requests.post(self.url, headers=self.headers, data=self.payload, files=files, timeout=self.timeout)
        data = response.json()

        # Check confidence score
        confidence = data["confidence"]
        self.logger.debug(f"Confidence: {confidence}")
        if confidence is not None and confidence >= confidence_threshold:
            return data
        else:
            raise ValueError(f"Confidence insufficient: {confidence} < {confidence_threshold}")
