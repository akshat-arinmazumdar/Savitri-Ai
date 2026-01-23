import requests
import json

API_KEY = "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"
MODEL = "mistralai/Mistral-7B-Instruct-v0.3"

urls = [
    "https://router.huggingface.co/hf-inference/v1/chat/completions",
    "https://router.huggingface.co/hf-inference/models/" + MODEL,
    "https://router.huggingface.co/v1/chat/completions",
    "https://api.huggingface.co/inference/v1/chat/completions"
]

for url in urls:
    print(f"Testing {url}...")
    try:
        data = {
            "model": MODEL,
            "messages": [{"role": "user", "content": "test"}],
            "max_tokens": 10
        }
        res = requests.post(url, headers={"Authorization": f"Bearer {API_KEY}"}, json=data, timeout=5)
        print(f"  Result: {res.status_code}")
        if res.status_code == 200:
            print(f"  ✅ FOUND WORKING URL: {url}")
            break
    except Exception as e:
        print(f"  Error: {str(e)}")
