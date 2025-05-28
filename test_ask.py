import requests

def test_bot():
    url = "http://127.0.0.1:8000/ask"
    payload = {"query": "What is metacognition?"}
    response = requests.post(url, json=payload)
    print("\n--- RESPONSE ---\n", response.json())

if __name__ == "__main__":
    test_bot()
