import os
import requests
import json
from dotenv import load_dotenv
import random
from database.chats import get_chat_history  # ✅ Already implemented in your chats.py

load_dotenv()

API_KEY = os.getenv("API_KEY")
MODEL = "gemini-2.0-flash"
API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent?key={API_KEY}"

# 🔹 Greeting check
def is_greeting(query: str) -> bool:
    greetings = ["hi", "hello", "hey", "good morning", "good evening", "namaste"]
    return query.lower().strip() in greetings

# 🔹 Motivational quote options
MOTIVATIONAL_NUDGES = [
    "You're one step closer to cracking UGC NET!",
    "Let’s make this study session count.",
    "Stay focused and keep pushing forward!",
    "You've got this! Let's tackle Paper 1 together.",
    "Keep learning, keep growing!"
]


def get_motivational_nudge() -> str:
    return random.choice(MOTIVATIONAL_NUDGES)

# 🔹 Build prompt — handles both academic queries and greetings
def build_prompt(query: str, context_chunks: list, user_id: str = None) -> str:
    if is_greeting(query):
        is_returning = False
        try:
            history = get_chat_history(user_id)
            is_returning = len(history) > 0
        except Exception as e:
            print(f"[History Error] Could not fetch chat history for greeting: {str(e)}")

        greeting = "Welcome back!" if is_returning else "Hi there!"
        nudge = get_motivational_nudge()

        return (
            "You are OwlAI, a friendly UGC NET assistant. The user greeted you casually.\n"
            "Respond in a warm, short sentence.\n"
            "If they are returning, say 'Welcome back!'. Always include one motivational line.\n\n"
            f"User: {query}\n"
            f"OwlAI: {greeting} I’m OwlAI, here to help you with UGC NET Paper 1. {nudge}"
        )

    if not context_chunks:
        context = "No prior context available."
    elif isinstance(context_chunks[0], str):
        context = "\n\n".join(context_chunks)
    else:
        context = "\n\n".join([c['metadata']['text'] for c in context_chunks])

    return (
        "You are OwlAI, a highly detailed assistant for UGC NET Paper 1.\n"
        "Answer all questions thoroughly in bullet points.\n"
        "Include explanations, elaborations, and relevant examples.\n"
        "Keep answers focused, clear, and educational.\n"
        "Even for basic queries, give 3–5 useful bullet points unless told otherwise.\n\n"
        f"Context:\n{context}\n\n"
        f"Question: {query}\n"
        "Answer:"
    )

# 🔹 Call Gemini API
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

            if not candidates or "content" not in candidates[0]:
                print("[LLM Error] No valid candidates.")
                return "Sorry, I couldn't generate a valid response."

            parts = candidates[0]["content"].get("parts", [])
            if not parts or "text" not in parts[0]:
                print("[LLM Error] No content parts.")
                return "Sorry, I couldn't generate a valid response."

            return "\n".join(p.get("text", "") for p in parts).strip()

        else:
            print(f"[LLM Error] {response.status_code}: {response.text}")
            return "Sorry, I couldn't generate a response due to an internal error."

    except Exception as e:
        print(f"[LLM Exception] {str(e)}")
        return "Sorry, I couldn't generate a response due to an unexpected error."

# 🔹 Clean response
def clean_llm_response(response: str) -> str:
    if "Answer:" in response:
        response = response.split("Answer:")[-1].strip()

    cleaned_lines = []
    for line in response.splitlines():
        if any(bad in line.lower() for bad in ["question", "option", "answers to the questions"]):
            continue
        cleaned_lines.append(line.strip())

    return "\n".join(cleaned_lines).strip()
