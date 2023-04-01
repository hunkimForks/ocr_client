import requests
import io
import logging
import json
import base64
import os


def get_confidence_score(data):
    result = json.loads(data["ocrResult"]["result"])
    return result.get("document_confidence")


def select_target_from_data(data, target):
    if target == 'text':
        words = json.loads(data["ocrResult"]["result"])["words"].values()
        return " ".join([v["transcription"] for v in words])
    elif target == 'text_with_coords':
        words = json.loads(data["ocrResult"]["result"])["words"].values()
        result = []
        for word in words:
            text = word["transcription"]
            coords = [(int(x), int(y)) for x, y in word["points"]]
            result.append({"text": text, "coordinates": coords})
        return result
    else:
        return data


def process_image(image):
    # Input is a byte string
    if isinstance(image, bytes):
        return image
    # Input is a filename
    elif isinstance(image, str) and os.path.isfile(image):
        return open(image, "rb")
    # Input is a base64 string
    elif isinstance(image, str) and image.startswith('data:image/'):
        return base64.b64decode(image.split(',')[1])
    else:
        raise ValueError('Invalid input: image must be a filename, byte string, or base64 string')


class UpOCRClient:
    def __init__(self, url: str, api_key: str, timeout=10, log_level: str="INFO"):
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
        # Process image
        try:
            files = {"image": process_image(image)}
        except Exception as e:
            self.logger.error("Failed during processing image: " + str(e))

        # Get response
        response = requests.post(self.url, headers=self.headers, files=files, timeout=self.timeout)

        # Check confidence score
        try:
            data = response.json()
            confidence = get_confidence_score(data)
            self.logger.debug(f"Confidence: {confidence}")
            if confidence is not None and confidence >= confidence_threshold:
                return select_target_from_data(data, target)
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
