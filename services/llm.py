# app/services/llm.py

import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")
MODEL = "gemini-2.0-flash"
API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent?key={API_KEY}"

def build_prompt(query: str, context_chunks: list) -> str:
    # context_chunks is a list of plain strings now, not objects
    context = "\n\n".join(context_chunks)
    return (
        f"You are OwlAI, a helpful assistant for UGC NET Paper 1.\n\n"
        f"Context:\n{context}\n\n"
        f"Question: {query}\n"
        f"Answer briefly in clear points with examples."
    )

def get_response_from_llm(prompt: str) -> str:
    headers = {"Content-Type": "application/json"}
    data = {
        "contents": [
            {
                "parts": [{"text": prompt}]
            }
        ]
    }

    response = requests.post(API_URL, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        json_data = response.json()
        return json_data["candidates"][0]["content"]["parts"][0]["text"].strip()
    else:
        raise ValueError(f"Error {response.status_code}: {response.text}")
