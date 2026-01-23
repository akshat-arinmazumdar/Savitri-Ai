import urllib.request
import json

urls = [
    "https://api-inference.huggingface.co/v1/chat/completions",
    "https://router.huggingface.co/v1/chat/completions",
    "https://router.huggingface.co/hf-inference/v1/chat/completions",
    "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.3/v1/chat/completions"
]

API_KEY = "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"

for url in urls:
    print(f"Testing: {url}")
    payload = {
        "model": "mistralai/Mistral-7B-Instruct-v0.3",
        "messages": [{"role": "user", "content": "test"}],
        "max_tokens": 5
    }
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data)
    req.add_header("Authorization", f"Bearer {API_KEY}")
    req.add_header("Content-Type", "application/json")
    req.add_header("User-Agent", "Mozilla/5.0")
    
    try:
        with urllib.request.urlopen(req) as response:
            print(f"✅ SUCCESS on {url}! Status: {response.status}")
            break
    except urllib.error.HTTPError as e:
        print(f"❌ Error {e.code}: {e.reason}")
    except Exception as e:
        print(f"❓ Unexpected Error type: {type(e).__name__} - {str(e)}")
