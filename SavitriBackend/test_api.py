import requests
import os

SERVER_URL = "http://127.0.0.1:8001"

def test_get_topics(filename):
    print(f"Testing topics for: {filename}")
    url = f"{SERVER_URL}/api/topics?filename={filename}"
    try:
        response = requests.get(url)
        print(f"Status Code: {response.status_code}")
        print("Response Body:")
        print(response.text)
    except Exception as e:
        print(f"Request failed: {e}")

if __name__ == "__main__":
    # Test with the filename seen in logs
    test_get_topics("DBMS_UNIT_2_Theory_.pdf")
