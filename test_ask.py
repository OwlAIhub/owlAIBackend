import requests

url = "http://127.0.0.1:8000/ask/"
headers = {"Content-Type": "application/json"}
payload = {
    "query": "What is ICT in education?",
    "user_id": "test_user"
}

response = requests.post(url, headers=headers, json=payload)
print("\n--- RESPONSE ---\n", response.json())
