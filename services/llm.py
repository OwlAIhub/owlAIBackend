import os
from services.session_memory import get_session_topic, get_last_aspect
from openai import OpenAI
from dotenv import load_dotenv
from services.language_detect import detect_language_hint

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
MODEL = "gpt-3.5-turbo-0125"

# 🔹 Friendly greeting detection
def is_greeting(query: str) -> bool:
    query = query.lower()
    greetings = ["hi", "hello", "hey", "good morning", "good evening", "namaste"]
    return any(greet in query for greet in greetings)

# 🔹 Tone detection
def detect_tone_hint(query: str) -> str:
    query = query.lower()
    if any(key in query for key in ["explain like", "simple terms", "like a kid"]):
        return "Use friendly language, analogies, and emojis if helpful."
    elif any(key in query for key in ["like a professor", "explain in detail", "deep dive"]):
        return "Use academic tone with technical detail."
    return ""

# 🔹 Generate contextual follow-up
def generate_followup_instruction(history_chunks: list) -> str:
    if not history_chunks:
        return "Offer a quiz, another example, or ask what they'd like to explore next."
    last_qna = history_chunks[-1] if isinstance(history_chunks[-1], str) else ""
    return f"Encourage continuation. Suggest quiz, deeper dive, or related topic. Context: {last_qna[:200]}..."

# 🔹 Generate friendly opener from context
def generate_opener_instruction(context_chunks: list, query: str) -> str:
    context_snippet = ""
    for c in context_chunks[-2:]:
        if isinstance(c, dict):
            text = c.get("metadata", {}).get("text", "")
            context_snippet += text + "\n"

    prompt = [
        {"role": "system", "content": "You are OwlAI. Based on the user’s last message and conversation, generate a warm, helpful opening sentence for your next reply. Keep it friendly, human, and natural — like a study buddy."},
        {"role": "user", "content": f"Previous:\n{context_snippet.strip()}\n\nCurrent User Query: {query}\n\nFriendly Opener:"}
    ]

    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=prompt,
            temperature=0.5
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"[Opener Generation Error] {e}")
        return "Let's get started with this one!"

# 🔹 Build the full prompt
def build_prompt(query: str, context_chunks: list, session_id: str = None, user_id: str = None, intent_tag: str = "academic") -> list:
    lang_hint = detect_language_hint(query)
    tone_hint = detect_tone_hint(query)

    context = "\n\n".join([
        c.get("metadata", {}).get("text", "") for c in context_chunks if isinstance(c, dict)
    ]) or "No prior context available."

    current_topic = get_session_topic(user_id or session_id)
    last_aspect = get_last_aspect(user_id or session_id)

    topic_info = ""
    if current_topic:
        topic_info += f"Current academic topic: {current_topic}.\n"
    if last_aspect:
        topic_info += f"Last discussed: {last_aspect}.\n"

    system_prompt = (
        "You are OwlAI — a warm, supportive, student-friendly assistant for UGC NET Paper 1.\n"
        "Act like a helpful teacher or study buddy. Be easy to talk to, use simple language, and keep things encouraging.\n"
        "You may use emojis, relatable examples, and real classroom scenarios to explain concepts.\n"
        f"{topic_info}{lang_hint}\n{tone_hint}"
    )

    followup_hint = generate_followup_instruction(context_chunks)
    opener = generate_opener_instruction(context_chunks, query)

    # 🔹 Casual
    if intent_tag == "casual":
        user_prompt = (
            f"The user greeted you casually.\n"
            f"Respond like a cheerful, informal study buddy (OwlAI).\n"
            f"Welcome them warmly and ask if they want to start with a quiz or learn something new.\n\n"
            f"User: {query}"
        )

    # 🔹 Emotional
    elif intent_tag == "emotional":
        user_prompt = (
            f"The user may feel stressed, confused, or overwhelmed.\n"
            f"Be kind and empathetic. Reassure them, and offer gentle steps to move forward.\n"
            f"Remind them they’re not alone in this.\n\n"
            f"User: {query}"
        )

    # 🔹 Academic and others
    else:
        user_prompt = (
            f"Context:\n{context}\n\n"
            f"User: {query}\n"
            f"---\n"
            f"Start your response with this friendly line:\n\"{opener}\"\n"
            f"Then follow this structure:\n"
            f"1. **Title/Heading**\n"
            f"2. 2–4 bullet points with key takeaways\n"
            f"3. A simple, relatable example\n"
            f"4. End with a motivating follow-up (quiz, examples, or what's next)\n"
            f"\nInstruction: {followup_hint}"
        )

    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]

# 🔹 Get response
def get_response_from_llm(prompt: list, intent_tag: str = "academic") -> str:
    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=prompt,
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"[OpenAI Error] {str(e)}")
        return "Sorry, I couldn’t generate a response due to a technical issue."

# 🔹 Clean LLM response
def clean_llm_response(response: str) -> str:
    cleaned_lines = [line.strip() for line in response.splitlines() if line.strip()]
    return "\n".join(cleaned_lines).strip()

# 🔹 Topic extraction
def extract_topic_via_llm(query: str) -> str:
    try:
        messages = [
            {"role": "system", "content": "You are OwlAI. Extract the UGC NET Paper 1 topic or subject the user is asking about (e.g., research aptitude, teaching aptitude, communication, etc.)."},
            {"role": "user", "content": f"Question: {query}\n\nTopic:"}
        ]
        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            temperature=0.3
        )
        return response.choices[0].message.content.strip().lower()
    except Exception as e:
        print(f"[Topic Extraction Error] {e}")
        return "ugc net"

# 🔹 Title generator
def generate_chat_title(user_question: str, bot_response: str) -> str:
    messages = [
        {"role": "system", "content": "You're OwlAI. Create a 3–6 word title for this UGC NET Paper 1 conversation."},
        {"role": "user", "content": f"User Question: {user_question}\nBot Answer: {bot_response}\n\nTitle:"}
    ]
    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            temperature=0.3
        )
        return response.choices[0].message.content.strip()[:60]
    except Exception as e:
        print(f"[Title Generation Error] {str(e)}")
        return user_question[:40]
