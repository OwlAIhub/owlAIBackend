# services/llm.py

import os
from openai import OpenAI
from dotenv import load_dotenv

from services.session_memory import get_session_state
from services.vector_search import query_vector_store

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
MODEL = "gpt-3.5-turbo"

def build_prompt(query, intent, tone, language, session_id, user_id):
    session = get_session_state(session_id)
    history = session.get("history", [])
    topic = session.get("active_topic", "UGC NET")

    # Vector context (if academic intent)
    context = ""
    if intent in ["concept_explanation", "chapter_teaching", "syllabus_query"]:
        chunks = query_vector_store(query)
        context ="\n\n".join([c.get("page_content", "") for c in chunks]) if chunks else ""

    system_prompt = f"""
You are OwlAI, a trusted and friendly UGC NET mentor. You help students in a structured, bilingual (Hindi/Hinglish/English) and motivating manner, based on their tone and intent.

Your responsibilities:
- Understand what the user wants (intent is already detected).
- If it’s a chapter/topic request, teach it step-by-step in parts.
- If it’s a quiz, walk them through interactively and handle scoring logically.
- If it’s emotional or motivational, support like a mentor.
- Follow up naturally and always provide the next best step.
- Never use overly generic phrases. Be specific, helpful, and human-like.

Tone: {tone}
Language: {language}
Intent: {intent}
Topic: {topic}
Query: {query}
Context: {context}
Recent conversation:
{history[-3:] if history else "None"}
"""

    messages = [
        {"role": "system", "content": system_prompt.strip()},
        {"role": "user", "content": query}
    ]

    return messages

def get_response_from_llm(prompt):
    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=prompt,
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print("[LLM ERROR]", str(e))
        return "Oops! Something went wrong while generating the response."

