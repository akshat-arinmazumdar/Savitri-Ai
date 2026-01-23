import urllib.request
import json

# We know these exist or are recommended
combinations = [
    "https://api-inference.huggingface.co/v1/chat/completions",
    "https://router.huggingface.co/hf-inference/v1/chat/completions",
    "https://router.huggingface.co/hf-inference/models/mistralai/Mistral-7B-Instruct-v0.3",
    "https://router.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.3",
    "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.3"
]

API_KEY = "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"

for url in combinations:
    print(f"Testing {url}...")
    
    if "chat/completions" in url:
        payload = {"model": "mistralai/Mistral-7B-Instruct-v0.3", "messages": [{"role": "user", "content": "hi"}], "max_tokens": 5}
    else:
        payload = {"inputs": "hi"}
        
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data)
    req.add_header("Authorization", f"Bearer {API_KEY}")
    req.add_header("Content-Type", "application/json")
    req.add_header("User-Agent", "Mozilla/5.0")
    
    try:
        with urllib.request.urlopen(req, timeout=5) as response:
            print(f"  ✅ SUCCESS! Status: {response.status}")
            print(f"  Working URL found: {url}")
            break
    except urllib.error.HTTPError as e:
        print(f"  ❌ Error {e.code}: {e.read().decode()[:100]}")
    except Exception as e:
        print(f"  ❓ {type(e).__name__}: {str(e)}")
