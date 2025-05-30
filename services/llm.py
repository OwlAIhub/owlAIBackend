import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")
MODEL = "gemini-2.0-flash"
API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent?key={API_KEY}"

def build_prompt(query: str, context_chunks: list) -> str:
    if not context_chunks:
        context = "No prior context available."
    elif isinstance(context_chunks[0], str):
        context = "\n\n".join(context_chunks)
    else:
        context = "\n\n".join([c['metadata']['text'] for c in context_chunks])

    return (
        "You are OwlAI, a highly detailed assistant for UGC NET Paper 1.\n"
        "Answer all questions thoroughly in bullet points.\n"
        "Include explanation, elaboration, and relevant examples where possible.\n"
        "Keep answers focused, well-structured, and educational.\n"
        "Even for simple queries, provide 3–5 clear bullet points unless explicitly told to be brief.\n\n"
        f"Context:\n{context}\n\n"
        f"Question: {query}\n"
        "Answer:"
    )


def get_response_from_llm(prompt: str) -> str:
    try:
        headers = {"Content-Type": "application/json"}
        data = {
            "contents": [{"parts": [{"text": prompt}]}]
        }

        response = requests.post(API_URL, headers=headers, data=json.dumps(data))

        if response.status_code == 200:
            json_data = response.json()
            candidates = json_data.get("candidates", [])

            print("[DEBUG] Raw Gemini response:", json_data)  # <- TEMP LOGGING

            if not candidates or "content" not in candidates[0]:
                print("[LLM Error] No valid candidates found.")
                return "Sorry, I couldn't generate a valid response."

            parts = candidates[0]["content"].get("parts", [])
            if not parts or "text" not in parts[0]:
                print("[LLM Error] No text found in response parts.")
                return "Sorry, I couldn't generate a valid response."

            return "\n".join(p.get("text", "") for p in parts).strip()


        else:
            print(f"[LLM Error] {response.status_code}: {response.text}")
            return "Sorry, I couldn't generate a response due to an internal error."

    except Exception as e:
        print(f"[LLM Exception] {str(e)}")
        return "Sorry, I couldn't generate a response due to an unexpected error."




def clean_llm_response(response: str) -> str:
    if "Answer:" in response:
        response = response.split("Answer:")[-1].strip()

    cleaned_lines = []
    for line in response.splitlines():
        if any(bad in line.lower() for bad in ["question", "option", "answers to the questions"]):
            continue
        cleaned_lines.append(line.strip())

    return "\n".join(cleaned_lines).strip()

