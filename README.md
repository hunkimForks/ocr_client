# Upstage Python SDK

## Installation

```bash
# install directly from GitHub
pip install git+https://github.com/UpstageAI/upstage.git

# get source and install
git clone https://github.com/UpstageAI/upstage.git
cd upstage
pip install .
```

## Usage

### OCR

```python
from upstage.api import OCR

api_key = "YOUR_UPSTAGE_API_KEY"
api_url = "https://ap-northeast-2.apistage.ai/document-ai/ocr"
filename = "/path/to/image.png"

client = OCR(api_url, api_key, log_level="DEBUG", timeout=10)
text = client.request(filename, "text")
print(text)
```

### Extractor

```python
from upstage.api import Extractor

document_type = "receipt"
api_key = "YOUR_UPSTAGE_API_KEY"
api_url = f"https://ap-northeast-2.apistage.ai/document-ai/extractor/{document_type}"
filename = "/path/to/image.png"

client = Extractor(api_url, api_key, log_level="DEBUG", timeout=10)
response = client.request(filename)
print(response.json())
```

## Testing

```bash
python -m unittest discover tests
```
