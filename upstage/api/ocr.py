import base64
import json
import logging
import os
import requests


def _get_confidence_score(data):
    result = json.loads(data["ocrResult"]["result"])
    return result.get("document_confidence")


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


def _select_target_from_data(data, target):
    if target == "text":
        words = json.loads(data["ocrResult"]["result"])["words"].values()
        return " ".join([v["transcription"] for v in words])
    elif target == "text_with_coords":
        words = json.loads(data["ocrResult"]["result"])["words"].values()
        result = []
        for word in words:
            text = word["transcription"]
            coords = [(int(x), int(y)) for x, y in word["points"]]
            result.append({"text": text, "coordinates": coords})
        return result
    else:
        return data


class OCR:
    def __init__(self, url: str, api_key: str, timeout=10, log_level="INFO"):
        """
        Initializes an instance of the OCR class.

        Args:
            url (str): The URL of the OCR API endpoint.
            api_key (str): The API key used to authenticate with the OCR API.
            timeout (int, optional): The number of seconds to wait for a response from the API (default is 10).
            log_level (str, optional): The logging level for the OCR instance (default is "INFO").

        Returns:
            None
        """
        # Set variables
        self.url = url
        self.api_key = api_key
        self.headers = {"Authorization": f"Bearer {self.api_key}"}
        self.timeout = timeout
        self.log_level = log_level

        # Set logger
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(level=self.log_level)

    def request(self, image, target=None, confidence_threshold=0.95) -> dict:
        """
        Requests Upstage OCR API on the input image and returns the result as a dictionary.

        Args:
            image (str or bytes): The input image as a filename or byte string, or a base64-encoded string.
            target (str, optional): The type of OCR result to return. Valid values are "text", "text_with_coords", or None (default). If "text", the result will be a string containing the transcribed text. If "text_with_coords", the result will be a list of dictionaries, where each dictionary contains the transcribed text and the coordinates of the bounding box for the corresponding word. If None, the full OCR result dictionary will be returned.
            confidence_threshold (float, optional): The minimum confidence score required for the OCR result to be considered valid. Must be a value between 0 and 1. Default is 0.95.

        Returns:
            dict: The OCR result as a dictionary.
        """
        try:
            # Process image
            files = {"image": _process_image(image)}

            # Get response
            response = requests.post(self.url, headers=self.headers, files=files, timeout=self.timeout)

            # Check confidence score
            data = response.json()
            confidence = _get_confidence_score(data)
            self.logger.debug(f"Confidence: {confidence}")
            if confidence is not None and confidence >= confidence_threshold:
                return _select_target_from_data(data, target)
            else:
                raise ValueError(f"Confidence insufficient: {confidence} < {confidence_threshold}")

        # Raise request error
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Upstage API request exception: {e}")
            return None

        # Raise any other error
        except Exception as e:
            self.logger.error(f"Upstage API failed: {e}")
            return None
