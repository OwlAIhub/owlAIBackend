# services/llm.py

import os
import json
from openai import OpenAI
from dotenv import load_dotenv
from services.vector_search import query_vector_store

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
MODEL = "gpt-3.5-turbo"

faculty_persona = """
You are OwlAI — a friendly, Hinglish-speaking UGC NET mentor for Tier 2/3 students.
Talk like a real faculty who explains topics in parts, checks understanding, gives quizzes, and never leaves a topic incomplete.
Your job is to teach students like they are beginners and support them like a buddy.
""".strip()


def build_prompt(query, intent, language, session_id, user_id):
    """
    Build a prompt based solely on the single active topic stored in session.
    Any session_state or learning_stage logic has been removed.
    """
    # Fetch the active topic from session
    from services.session_memory import get_session_state
    session = get_session_state(session_id)
    topic = session.get("active_topic", "UGC NET")

    # Pull context for that topic
    db_chunks = query_vector_store(topic)
    db_context = "\n\n".join(c.get("page_content", "") for c in db_chunks) or "No relevant notes found."


    persona = (
        f"You are chatting with user `{user_id}`.\n"
        f"The user’s intent is `{intent}`.\n"
        f"Please tailor your response accordingly.\n"
    )


    prompt_content = f"""
== 🧠 You are OwlAI ==
A Hinglish-speaking UGC NET mentor. Act like a real faculty.

== 🎯 Student Query ==
{query}

== 📚 Topic ==
{topic}
Language: {language}

== 📖 Study Material ==
{db_context}

Now, do the following based on the query:
- If the user asks for an explanation, explain {topic} in Hinglish in 4–5 bullet points.
- If they ask for a quiz, provide 2 MCQs with feedback.
- After your response, always ask: “Ready for the next topic or want to try a quiz?”
- Never break flow or wander off-topic.
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


def generate_quiz_questions(topic: str, num_questions: int = 5):
    system_prompt = f"""
You are OwlAI, a UGC NET mentor.

Generate exactly {num_questions} multiple-choice questions (MCQs) strictly related to the topic: "{topic}" for UGC NET Paper 1.

Format your response as a JSON array with each item structured like this:

{{
  "question": "What is teaching aptitude?",
  "options": ["A. Ability to teach", "B. Ability to dance", "C. Ability to sing", "D. Ability to cook"],
  "answer": "A"
}}

🚫 Do not add explanations, extra text, or comments.
✅ Only output a JSON array of questions.
""".strip()

    messages = [{"role": "system", "content": system_prompt}]
    response = get_response_from_llm(messages)

    try:
        return json.loads(response)
    except Exception as e1:
        print("[QUIZ ERROR] Initial parse failed:", e1)
        fallback_prompt = [
            {"role": "system", "content": "Please reformat the quiz strictly as a JSON array like this:"},
            {"role": "user", "content": response}
        ]
        fallback_response = get_response_from_llm(fallback_prompt)
        try:
            return json.loads(fallback_response)
        except Exception as e2:
            print("[QUIZ ERROR] Fallback also failed:", e2)
            return []


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
- Any quiz they participated in
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


def generate_quiz_step_response(user_answer, quiz_state, tone, language):
    questions = quiz_state["questions"]
    index = quiz_state["current_index"]

    if index >= len(questions):
        return "🎉 Quiz complete! Great job!"

    current_q = questions[index]
    correct_option = current_q["answer"].strip().upper()

    response = f"Question {index + 1}: {current_q['question']}\n"
    for opt in current_q["options"]:
        response += f"{opt}\n"

    if user_answer is not None:
        cleaned = user_answer.strip().upper()
        is_correct = cleaned == correct_option
        quiz_state.setdefault("answers", []).append({
            "question": current_q["question"],
            "user_answer": cleaned,
            "correct_answer": correct_option,
            "is_correct": is_correct
        })
        response += "\n✅ Sahi jawab! Well done!" if is_correct else f"\n❌ Galat jawab. Correct answer: {correct_option}"
        quiz_state["current_index"] += 1
    else:
        response += "\n\nPlease choose your answer (A/B/C/D):"

    return response


def generate_followup_prompt(session_id: str) -> str:
    from services.session_memory import get_session_state

    session = get_session_state(session_id)
    topic = session.get("active_topic", "UGC NET")

    prompt = f"""
You are OwlAI — a friendly UGC NET faculty.

The student has just covered: {topic}

Suggest ONE next step in Hinglish:
- “Shall we try a quick quiz on {topic}?”
- “Ready for the next topic?”
- “Would you like a quick summary again?”

Keep it short and warm.
""".strip()

    return get_response_from_llm([{"role": "system", "content": prompt}])
