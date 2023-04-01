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

## Run

```python
from upstage.api import OCR

api_key = "YOUR_UPSTAGE_API_KEY"
api_url = "https://ap-northeast-2.apistage.ai/document-ai/ocr"
filename = "/path/to/image.png"

client = OCR(api_url, api_key, log_level="DEBUG", timeout=10)
text = client.request(filename, "text")
print(text)
```
