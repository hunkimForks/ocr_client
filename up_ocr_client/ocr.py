import base64
import json
import logging
import os
import requests


def get_confidence_score(data):
    result = json.loads(data["ocrResult"]["result"])
    return result.get("document_confidence")


def process_image(image):
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


def select_target_from_data(data, target):
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


class UpOCRClient:
    def __init__(self, url: str, api_key: str, timeout=10, log_level="INFO"):
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
        try:
            # Process image
            files = {"image": process_image(image)}

            # Get response
            response = requests.post(self.url, headers=self.headers, files=files, timeout=self.timeout)

            # Check confidence score
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
