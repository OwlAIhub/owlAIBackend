import os
from openai import OpenAI
from dotenv import load_dotenv
from services.vector_search import query_vector_store

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
MODEL = "gpt-3.5-turbo"

faculty_persona = """
You are OwlAI — a warm, friendly, and helpful UGC NET mentor who speaks natural Hinglish like a real faculty from Tier 2/3 cities.

🚫 Never use:
- Over-casual words like “chal”, “tujhe”, “main samjha deta hoon”
- Informal tone like “tu”, “tera”, etc.
- Self-appraising lines like “I explained it well” or “you’re doing great!” unless it feels natural

✅ Always:
- Use polite Hinglish — like a caring teacher
- Keep it real, supportive, and simple
- Use light classroom examples or analogies
- Avoid robotic tone or textbook-style Hindi like "uddheshyapurn", "vishleshan", etc.

""".strip()


def build_prompt(query, intent, language, session_id, user_id, name=None):
    from services.session_memory import get_session_state
    session = get_session_state(session_id)
    topic = session.get("active_topic", "UGC NET")

    if intent in ["chapter_teaching", "concept_explanation"]:
        db_chunks = query_vector_store(topic)
        db_context = "\n\n".join(c.get("page_content", "") for c in db_chunks) or "No relevant notes found."
    else:
        db_context = ""

    greeting_line = f"Namaste {name}!" if name else ""
    greeting_section = f"==  Greet ==\n{greeting_line}\n\n" if greeting_line else ""

    persona_context = (
        f"You are chatting with user `{user_id}`.\n"
        f"The user’s intent is `{intent}` and preferred language is `{language}`.\n"
        f"Use Hinglish naturally and avoid hard words.\n"
        f"Stick to casual tone — not textbook tone.\n"
    )

    if intent == "concept_explanation":
        task_instruction = f"""
        - Explain **{topic}** using easy Hinglish and 4–5 simple points.
        - Use daily-life ya classroom examples.
        - Keep it student-friendly and engaging.
        """
    elif intent in ["emotion", "motivational"]:
        task_instruction = """
        - Give friendly motivation in Hinglish.
        - Remind them: progress > perfection.
        - Keep it student-friendly and engaging.
        """
    else:
        task_instruction = """
        - Answer using Hinglish, in a natural tone.
        - Keep it real — avoid robotic/formal lines.
        - Keep it student-friendly and engaging.
        """

    prompt_content = f"""
== You are OwlAI ==
UGC NET mentor, explaining in easy Hinglish, like a real teacher.

{greeting_section}

==  Student Query ==
{query}

==  Topic ==
{topic}


==  Study Material ==
{db_context if db_context else "No extra notes needed for this query."}

==  Reminder ==
This chat is private — just between OwlAI and the student. Guide them with warmth and clarity.

==  Instructions ==
{task_instruction.strip()}
""".strip()

    return [
        {"role": "system", "content": faculty_persona + "\n\n" + persona_context},
        {"role": "user", "content": prompt_content}
    ]


def get_response_from_llm(prompt):
    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=prompt,
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print("[LLM ERROR]", e)
        return "Oops! Kucch galat ho gaya. Thoda try karo dobara!"


def generate_session_summary(session_id: str) -> str:
    from services.session_memory import get_session_state

    session = get_session_state(session_id)
    topic = session.get("active_topic", "UGC NET Paper 1")
    history = session.get("history", [])

    if not history:
        return "Ab tak koi discussion nahi hui. Aaiye shuruaat karte hain! 😊"

    chat_log = ""
    for pair in history:
        user_q = pair.get("query", "").strip()
        bot_a = pair.get("response", "").strip()
        if user_q and bot_a:
            chat_log += f"\n👤 User: {user_q}\n🦉 OwlAI: {bot_a}\n"

    prompt = f"""
== 🧠 You are OwlAI ==
A warm, Hinglish mentor helping with UGC NET Paper 1.

== 🎯 Task ==
Give a natural, casual summary of what the student has covered so far.

== 💬 Chat History ==
Topic: {topic}
{chat_log}

== 📋 Output Guidelines ==
 - Use a warm Hinglish tone, as if you're recapping the student's progress in a friendly, motivating way.
 - Don't repeat their queries or full responses. Just extract the key concepts and progress made.
 - Summarize the main themes, concepts, or subtopics covered so far.
 - Encourage the student to move forward or ask questions next — without using the same fixed sentence every time.
 - Avoid robotic or templated lines. Be human-like, varied, and natural.
"""

    return get_response_from_llm([
        {"role": "system", "content": "Summarize student learning so far in easy, non-repetitive Hinglish."},
        {"role": "user", "content": prompt}
    ])


def generate_followup_prompt(session_id: str) -> str:
    from services.session_memory import get_session_state

    session = get_session_state(session_id)
    topic = session.get("active_topic", "UGC NET")
    history = session.get("history", [])[-3:]

    formatted_history = "\n".join([
        f"User: {msg['query']}\nOwlAI: {msg['response']}" for msg in history
    ])

    followup_prompt = [
        {
            "role": "system",
            "content": """
 You are OwlAI — a warm, friendly UGC NET teacher.
You speak like a human teacher, but do not specify your gender.

 Based on the current response, what is the most engaging thing OwlAI could say to keep the student motivated and learning?

Your job is to keep the student engaged and curious — but stay natural.

- Avoid overpraising the student or sounding robotic.
- Don't reflect on your own answers.
- Instead, ask something smart, interesting, or short to keep the learning moving.
- Use Hinglish in a clear and human tone, as if a teacher is talking to a student in class.
- keep it short

No “main bata deta hoon”, no “you’re doing great!” unless it naturally fits.

"""
        },
        {
            "role": "user",
            "content": f"== Chat History ==\n{formatted_history}\n\n== Topic ==\n{topic}"
        }
    ]

    return get_response_from_llm(followup_prompt)


def generate_chat_title(query: str, response: str) -> str:
    prompt = [
        {"role": "system", "content": "You are OwlAI — an academic chatbot. Create a short, clear title (max 10 words) that fits the question and answer. Keep it human, not robotic."},
        {"role": "user", "content": f"User asked: {query}\n\nBot replied: {response}"}
    ]
    try:
        reply = client.chat.completions.create(
            model=MODEL,
            messages=prompt,
            temperature=0.5
        )
        return reply.choices[0].message.content.strip().replace('"', '').removeprefix("Title:").strip()
    except Exception as e:
        print("[TITLE ERROR]", e)
        return query[:40]
