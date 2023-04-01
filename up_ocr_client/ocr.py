import requests
import io
import logging
import json
import base64


class UpOCRClient:
    def __init__(self, url: str, api_key: str, timeout=10, log_level: str="INFO"):
        self.url = url
        self.api_key = api_key
        self.timeout = timeout
        self.log_level = log_level

        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(level=self.log_level)

    def request(self, img_filename=None, img_bytes=None, image_base64=None, img_format=""):
        headers = {"api_key": self.api_key}
        response_json = {}

        try:
            if img_filename:
                img_bytes = open(img_filename, "rb")
            elif image_base64:
                img_bytes = io.BytesIO(base64.b64decode(image_base64))
        except Exception as e:
            self.logger.error("UpOCR failed: " + str(e))

        if img_bytes is None:
            raise Exception("No image data provided")

        file_tuple = ("file", img_bytes, f"image/{img_format}")
        payload = {"image": file_tuple}

        try:
            response = requests.post(
                self.url, files=payload, headers=headers, timeout=self.timeout
            )

            response.raise_for_status()
            response_json = response.json()
        except requests.exceptions.RequestException as e:
            self.logger.error("UpOCR failed: " + str(e))
            response = None
        except Exception as e:
            self.logger.error("UpOCR failed: " + str(e))
            response = None

        # TODO: Lucy, please raise exception if confidence is too low

        return response_json

    def get_text(self,  img_filename=None, img_bytes=None, image_base64=None) -> str:
        ocr_data = self.request(
            img_filename=img_filename, img_bytes=img_bytes, image_base64=image_base64)
        if ocr_data is None:
            return ""

        if ocr_data["ok"]:
            parsed = json.loads(ocr_data["ocrResult"]["result"])
            all_words = [v["transcription"] for v in parsed["words"].values()]
            return " ".join(all_words)

        return ""

    def get_text_with_coors(self,  img_filename=None, img_bytes=None, image_base64=None) -> list:
        result = []
        ocr_data = self.request(
            img_filename=img_filename, img_bytes=img_bytes, image_base64=image_base64)

        if ocr_data is None:
            return result

        if not ocr_data["ok"]:
            return result

        ocr_result = json.loads(ocr_data["ocrResult"]["result"])["words"]

        for _, value in ocr_result.items():
            text = value["transcription"]
            coordinates = value["points"]
            coordinates_int = [(int(x), int(y)) for x, y in coordinates]
            result.append({"text": text, "coordinates": coordinates_int})
        return result
