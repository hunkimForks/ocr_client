import base64
import os


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
