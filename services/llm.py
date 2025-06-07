import os
from openai import OpenAI
from dotenv import load_dotenv
from services.session_memory import get_session_topic

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
MODEL = "gpt-3.5-turbo-0125"

def build_persona_prompt(language, tone, intent, last_topic=None) -> str:
    base = (
        "You are OwlAI — a friendly, emotionally intelligent tutor for UGC NET Paper 1 students.\n"
        "You explain clearly, with relatable analogies, and you speak like a helpful senior.\n"
        "You adjust based on user mood, intent, and language preference.\n"
        "Avoid using food/kitchen/chef analogies. They are overused and not relevant.\n"
    )

    if intent == "quiz_start":
        base += "You are in quizmaster mode. Be energetic and clear. Ask one MCQ at a time.\n"
    elif intent == "emotional":
        base += "The user may be feeling low or anxious. Speak gently and offer encouragement.\n"
    elif intent == "rephrase":
        base += "Simplify the explanation in casual, friendly Hinglish.\n"

    if tone == "simple":
        base += "Use short sentences, Hinglish if appropriate, emojis if they feel natural.\n"
    elif tone == "detailed":
        base += "Use technical details and formal explanation with examples.\n"

    if language == "HINGLISH":
        base += (
            "Speak in Hinglish like: ‘chalo start karte hain’, ‘ab samjha kya’, ‘tu kar lega bhai’. "
            "Avoid formal tone. Be like a desi senior.\n"
        )
    elif language == "HINDI":
        base += "Use pure but simple Hindi. Be polite and helpful.\n"
    else:
        base += "Use polite, encouraging English. Avoid being robotic.\n"

    if last_topic:
        base += f"Current academic topic is: {last_topic}\n"

    return base



def generate_followup_instruction(history: list) -> str:
    if not history:
        return "Ask if they'd like a quiz, more examples, or another topic."
    last = history[-1]
    context = "\n".join(f"Q: {h['q']}\nA: {h['a']}" for h in history[-3:] if h.get("q") and h.get("a"))
    prompt = [
        {"role": "system", "content": (
            "You're OwlAI. Suggest a smart, friendly follow-up line (quiz, example, new topic, etc.) based on recent chat."
        )},
        {"role": "user", "content": f"{context}\n\nLast: {last['q']}\nResponse: {last['a']}"}
    ]
    try:
        response = client.chat.completions.create(model=MODEL, messages=prompt, temperature=0.7)
        return response.choices[0].message.content.strip()
    except Exception:
        return "Wanna do a quiz or move to the next topic?"

def build_prompt(query, history=[], context=[], session_id=None, user_id=None, intent="academic", tone="neutral", language="ENGLISH") -> list:
    current_topic = get_session_topic(user_id or session_id)
    persona = build_persona_prompt(language, tone, intent, last_topic=current_topic)
    followup = generate_followup_instruction(history)

    chat_context = "\n\n".join([f"Q: {h['q']}\nA: {h['a']}" for h in history])
    rag_context = "\n".join(c.get("metadata", {}).get("text", "") for c in context)

    user_prompt = f"\nUser: {query}\n\nChat Context:\n{chat_context}\n\nExtra Context:\n{rag_context}\n\n{followup}"

    return [
        {"role": "system", "content": persona},
        {"role": "user", "content": user_prompt}
    ]

def get_response_from_llm(prompt):
    try:
        response = client.chat.completions.create(model=MODEL, messages=prompt, temperature=0.65)
        return response.choices[0].message.content.strip()
    except Exception:
        return "Sorry, I couldn’t process that. Want to try again?"

def clean_response(text):
    return "\n".join([line.strip() for line in text.splitlines() if line.strip()])
