import os
import io
import base64
from up_ocr_client.ocr import UpOCRClient

# Initialize the client
BACKEND_URL = os.environ["OCR_BACKEND_URL"]
SECRET = os.environ["OCR_SECRET"]
client = UpOCRClient(BACKEND_URL, SECRET)


def test_ocr_get_text():
    file_path = os.path.join(os.path.dirname(__file__), "data", "upstage.png")

    with open(file_path, "rb") as f:
        img_data = io.BytesIO(f.read())

    text = client.get_text(img_data)
    assert isinstance(text, str)


def test_ocr_get_text_with_coors():
    file_path = os.path.join(os.path.dirname(__file__), "data", "upstage.png")

    with open(file_path, "rb") as f:
        img_data = io.BytesIO(f.read())

    text_with_coors = client.get_text_with_coors(img_data)
    assert isinstance(text_with_coors, list)


def test_ocr_up_ocr():
    file_path = os.path.join(os.path.dirname(__file__), "data", "upstage.png")

    with open(file_path, "rb") as f:
        image_base64 = base64.b64encode(f.read()).decode("utf-8")

    text_from_base64 = client.ca(image_base64)
    assert isinstance(text_from_base64, str)


def test_input_types():
    # Set the image file path
    img_filename = os.path.join(
        os.path.dirname(__file__), "data", "upstage.png")

    # Read the image file
    with open(img_filename, "rb") as f:
        img_bytes = f.read()

    # Convert the image bytes to base64
    image_base64 = base64.b64encode(img_bytes).decode()

    # Test case 1: img_filename
    text = client.get_text(img_filename=img_filename)
    print("Extracted text using img_filename: ", text)

    # Test case 2: img_bytes
    text = client.get_text(img_bytes=img_bytes)
    print("Extracted text using img_bytes: ", text)

    # Test case 3: image_base64
    text = client.get_text(image_base64=image_base64)
    print("Extracted text using image_base64: ", text)
