import logging
import requests

from ..utils import _process_image


def _get_confidence_score(data):
    return data["confidence"]


def _select_target_from_data(data, target):
    if target == "text":
        return data["text"]
    elif target == "text_with_coords":
        words = data["pages"][0]["words"]
        result = []
        for word in words:
            coords = [(coord["x"], coord["y"]) for coord in word["boundingBox"]["vertices"]]
            result.append({"text": word["text"], "coordinates": coords})
        return result
    else:
        return data


class OCR:
    def __init__(self, url: str, api_key: str, redact=False, timeout=10, log_level="INFO"):
        """
        Initializes an instance of the OCR class.

        Args:
            url (str): The URL of the OCR API endpoint.
            api_key (str): The API key used to authenticate with the OCR API.
            redact (bool, optional): Whether to redact sensitive information from the OCR result. Default is False.
            timeout (int, optional): The number of seconds to wait for a response from the API (default is 10).
            log_level (str, optional): The logging level for the OCR instance (default is "INFO").

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
            response = requests.post(self.url, headers=self.headers, data=self.payload, files=files, timeout=self.timeout)
            data = response.json()

            # Check confidence score
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
