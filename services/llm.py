# services/llm.py

import os
from openai import OpenAI
from dotenv import load_dotenv
import json

from services.session_memory import get_session_state
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
    session = get_session_state(session_id)
    state = session.get("learning_state", {
        "current_unit": "UGC NET",
        "current_subtopic": "Introduction",
        "learning_stage": "explanation",
        "has_done_quiz": False,
        "last_question_type": "None"
    })

    current_unit = state["current_unit"]
    current_subtopic = state["current_subtopic"]

    # 🔎 Pull topic-specific content
    db_chunks = query_vector_store(f"{current_unit} {current_subtopic}")
    db_context = "\n\n".join([c.get("page_content", "") for c in db_chunks]) or "No relevant notes found."

    # ✅ Strong formatting
    prompt_content = f"""
== 🧠 You are OwlAI ==
A Hinglish-speaking UGC NET mentor. Act like a real faculty.

== 🎯 Student Query ==
{query}

== 📚 Context ==
Unit: {current_unit}
Sub-topic: {current_subtopic}
Stage: {state['learning_stage']}
Quiz done? {state['has_done_quiz']}
Language: {language}

== 📖 Study Material ==
{db_context}

Now, do the following based on the query:
- If user is learning a topic, explain one subtopic only, in Hinglish, in 4–5 bullet points or more if required
- If user has already read a topic, give 2 MCQs with feedback to check for the topic preparation
- After every topic, ask “Ready for the next topic or want to try a quiz?”
- If user is emotional or demotivated, respond like a friend and mentor
- NEVER break flow. Stick to the topic unless the user clearly changes it or the topic has been covered by the user

""".strip()

    return [
        {"role": "system", "content": "You are OwlAI, a UGC NET faculty-mode mentor."},
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
        print("[LLM ERROR]", str(e))
        return "Oops! Something went wrong while generating the response."

# llm.py

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

    # Step 1: Try once
    response = get_response_from_llm(messages)
    try:
        return json.loads(response)
    except Exception as e1:
        print("[QUIZ ERROR] Initial parse failed:", e1)

        # Step 2: Retry with formatting instruction if GPT returns non-JSON
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
        return "Abhi tak koi detailed conversation nahi hua hai. Let’s begin with a topic!"

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

Be short, human, and direct. Speak **to** the student (not about them).
"""},
        {"role": "user", "content": f"Here's our recent chat (topic: {topic}):\n\n{formatted_chat}"}
    ]

    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=prompt,
            temperature=0.7
        )
        return response.choices[0].message.content.strip()

    except Exception as e:
        print("[SUMMARY ERROR]", str(e))
        return "I couldn't generate a summary at the moment. Try again later."



    


  # Make sure this works with OpenAI or fallback model

def generate_quiz_step_response(user_answer, quiz_state, tone, language):
   
    questions = quiz_state["questions"]
    index = quiz_state["current_index"]

    # Handle edge cases
    if index >= len(questions):
        return "🎉 Quiz complete! Great job!"

    current_q = questions[index]

    # Prepare the feedback content
    correct_option = current_q["answer"].strip().upper()
    response = f"Question {index + 1}: {current_q['question']}\n"
    for opt in current_q["options"]:
        response += f"{opt}\n"

    # Evaluate the user answer if provided
    if user_answer is not None:
        cleaned_answer = user_answer.strip().upper()
        is_correct = cleaned_answer == correct_option

        # Safely initialize the answers list if not present
        if "answers" not in quiz_state:
            quiz_state["answers"] = []

        quiz_state["answers"].append({
            "question": current_q["question"],
            "user_answer": cleaned_answer,
            "correct_answer": correct_option,
            "is_correct": is_correct
        })

        # Add feedback message
        if is_correct:
            response += "\n✅ Sahi jawab! Well done!"
        else:
            response += f"\n❌ Galat jawab. The correct answer is: {correct_option}"

        # Move to next question index only after an answer
        quiz_state["current_index"] += 1
    else:
        response += "\n\nPlease choose your answer (A/B/C/D):"

    return response





def generate_followup_prompt(session_id: str) -> str:
    from services.session_memory import get_learning_state

    state = get_learning_state(session_id)
    unit = state.get("current_unit", "UGC NET")
    subtopic = state.get("current_subtopic", "Introduction")
    quiz_done = state.get("has_done_quiz", False)
    stage = state.get("learning_stage", "explanation")

    next_prompt = f"""
You are OwlAI — a friendly UGC NET faculty.

The student is currently on:
- Unit: {unit}
- Sub-topic: {subtopic}
- Quiz done: {'Yes' if quiz_done else 'No'}
- Stage: {stage}

Respond in Hinglish, and suggest one thing:
- “Shall we try a quick quiz on this?”
- “Move to next sub-topic?”
- “Want to repeat this once again?”
Choose only one follow-up and keep it short.
""".strip()

    return get_response_from_llm([{"role": "system", "content": next_prompt}])
