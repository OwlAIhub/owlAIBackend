import os
from openai import OpenAI
from dotenv import load_dotenv
from services.vector_search import query_vector_store

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
MODEL = "gpt-3.5-turbo"

faculty_persona = """
You are OwlAI — a warm, Hinglish-speaking UGC NET mentor for Tier 2/3 students.

You behave like a real faculty who:
- teaches slowly, step by step
- uses Hinglish naturally, unless the user asks otherwise
- uses examples from classroom or everyday life
- explains topics like the student is a beginner.
- offers summaries to keep learning continuous
- never leaves a topic incomplete
- avoids complex jargon unless needed, and explains it if used
- adapts to the user's mood (motivational, confused, excited, etc.)
""".strip()


def build_prompt(query, intent, language, session_id, user_id, name=None, ):
    from services.session_memory import get_session_state
    session = get_session_state(session_id)
    topic = session.get("active_topic", "UGC NET")

    # RAG only for academic intents
    if intent in ["chapter_teaching", "concept_explanation"]:
        db_chunks = query_vector_store(topic)
        db_context = "\n\n".join(c.get("page_content", "") for c in db_chunks) or "No relevant notes found."
    else:
        db_chunks = []
        db_context = ""
        
    
    greeting_line = f"Namaste {name}!" if name else ""
    greeting_section = f"==  Greet ==\n{greeting_line}\n\n" if greeting_line else ""



    persona = (
        f"You are chatting with user `{user_id}`.\n"
        f"The user’s intent is `{intent}`.\n"
        f"Please tailor your response accordingly.\n"
    )

    # Instruction varies by intent
    if intent == "concept_explanation":
        task_instruction = f"""
        - Explain the topic **{topic}** in Hinglish using 4–5 simple bullet points.
        - Use examples from daily life or classroom.
        - End with: ““Want to move to next concept?” or "want to deep dive into {topic}".
        """
    elif intent in ["emotion", "motivational"]:
        task_instruction = """
        - Motivate the student in Hinglish.
        - Use friendly, human tone.
        - Remind them that progress matters more than perfection.
        - End with: “Chalein, thoda aur padhein?”
        """
    else:
        task_instruction = """
        - Answer the query in Hinglish.
        - Use academic reasoning if needed.
        """

    # Build prompt content
    prompt_content = f"""
== You are OwlAI ==
A Hinglish-speaking UGC NET mentor. Act like a real faculty.


{greeting_section}

==  Student Query ==
{query}

==  Topic ==
{topic}
Language: {language}

==  Study Material ==
{db_context if db_context else "No notes needed for this query."}

==  Reminder ==
This chat is private and secure — no one can access it except you and OwlAI.
OwlAI is created by students and teachers who’ve been in your shoes — here to help you crack UGC NET Paper 1 with warmth and clarity.

==  Instructions ==
{task_instruction.strip()}
""".strip()

    return [
        {"role": "system", "content": faculty_persona + "\n\n" + persona},
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
        return "Oops! Something went wrong while generating the response."


def generate_session_summary(session_id: str) -> str:
    from services.session_memory import get_session_state

    session = get_session_state(session_id)
    history = session.get("history", [])
    topic = session.get("active_topic", "UGC NET")

    if not history:
        return "Abhi tak koi conversation nahi hui hai. Let’s begin!"

    formatted_chat = "\n".join([
        f"User: {h['query']}\nOwlAI: {h['response']}" for h in history[-10:]
    ])

    prompt = [
        {"role": "system", "content": """
You are OwlAI – a helpful and warm UGC NET mentor.

Summarize your recent learning journey with the student in second-person tone.

Mention:
- What the student asked or learned
- What you explained
- Encourage what they can do next

Be short, human, and direct. Speak to the student.
"""},
        {"role": "user", "content": f"Topic: {topic}\n\n{formatted_chat}"}
    ]

    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=prompt,
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print("[SUMMARY ERROR]", e)
        return "I couldn't generate a summary at the moment. Try again later."


def generate_followup_prompt(session_id: str) -> str:
    from services.session_memory import get_session_state

    session = get_session_state(session_id)
    topic = session.get("active_topic", "UGC NET")
    history = session.get("history", [])[-3:]  # last 3 messages

    # Format history into readable string
    formatted_history = "\n".join([
        f"User: {msg['query']}\nOwlAI: {msg['response']}" for msg in history
    ])

    followup_prompt = [
        {
            "role": "system",
            "content": """
You are OwlAI — a warm, friendly UGC NET teacher.
You speak like a human teacher, but do not specify your gender.

Based on the recent conversation with the student, suggest one natural next step they might take. Keep it short, warm, and interactive.

Possibilities: offer summary, suggest next topic, or just encouragement to continue.

Always use Hinglish.
"""
        },
        {
            "role": "user",
            "content": f"""
== Conversation History ==
{formatted_history}

== Current Topic ==
{topic}

What would be the best next suggestion?
"""
        }
    ]

    return get_response_from_llm(followup_prompt)


def generate_chat_title(query: str, response: str) -> str:
    prompt = [
        {"role": "system", "content": "You are OwlAI — an academic chatbot for UGC NET. Generate a short and clear title (max 10 words) for the user's question and your answer."},
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
