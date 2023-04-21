# Upstage Python SDK

## Usage

```python
from upstage.api import Extractor, OCR

api_key = "YOUR_UPSTAGE_API_KEY"
filename = "/path/to/image.png"

# ocr
api_url = "https://ap-northeast-2.apistage.ai/document-ai/ocr"
client = OCR(api_url, api_key, log_level="DEBUG", timeout=10)
text = client.request(filename, "text")
print(text)

# extractor
document_type = "receipt"
api_url = f"https://ap-northeast-2.apistage.ai/document-ai/extractor/{document_type}"
client = Extractor(api_url, api_key, log_level="DEBUG", timeout=10)
response = client.request(filename)
print(response.json())
```

## Testing

```bash
python -m unittest discover tests
```
