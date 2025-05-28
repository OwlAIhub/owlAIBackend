# services/llm.py

import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")
MODEL = "gemini-2.0-flash"
API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent?key={API_KEY}"

def build_prompt(query: str, context_chunks: list) -> str:
    """
    Builds a structured prompt using either raw text chunks or metadata dicts.
    """
    # Determine if context_chunks are strings or dicts
    if isinstance(context_chunks[0], str):
        context = "\n\n".join(context_chunks)
    else:
        context = "\n\n".join([c['metadata']['text'] for c in context_chunks])

    return (
        "You are OwlAI, a helpful assistant for UGC NET Paper 1.\n"
        "You will receive a user question and some background context.\n"
        "Use only the relevant parts of the context to answer.\n"
        "Do NOT repeat the original context or list the questions again.\n"
        "Answer in clear, brief, point-wise format. Include examples only if helpful.\n\n"
        f"Context:\n{context}\n\n"
        f"Question: {query}\n"
        "Answer:"
    )


def get_response_from_llm(prompt: str) -> str:
    """
    Sends a prompt to Gemini LLM API and retrieves the response.
    """
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
        return json_data['candidates'][0]['content']['parts'][0]['text'].strip()
    else:
        return f"Error {response.status_code}: {response.text}"

def clean_llm_response(response: str) -> str:
    """
    Cleans up verbose or repeated parts from the LLM's raw output.
    """
    if "Answer:" in response:
        response = response.split("Answer:")[-1].strip()

    cleaned_lines = []
    for line in response.splitlines():
        if any(bad in line.lower() for bad in ["question", "option", "answer:", "answers to the questions", "**"]):
            continue
        cleaned_lines.append(line.strip())

    return "\n".join(cleaned_lines).strip()
