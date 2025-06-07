from fastapi import APIRouter
from pydantic import BaseModel

from services.llm import build_prompt, get_response_from_llm, clean_response
from services.intent_tone_classifier import classify_intent_tone_language
from services.quiz_generator import generate_quiz_questions
from services.session_memory import (
    get_quiz_state, start_quiz, update_quiz_state, reset_quiz,
    update_session_topic, set_last_mood, set_active_quiz_topic
)
from services.professional_handler import handle_professional_query
from services.vector_search import query_vector_store  # ✅ NEW IMPORT
from database.sessions import create_session
from database.chats import save_chat, get_chat_history_by_session

ask_router = APIRouter()

class AskRequest(BaseModel):
    session_id: str
    query: str
    user_id: str

@ask_router.post("/")
async def ask_question(req: AskRequest):
    query = req.query.strip()
    user_id = req.user_id.strip()
    session_id = req.session_id.strip() or create_session(user_id)

    meta = classify_intent_tone_language(query)
    intent = meta['intent']
    tone = meta['tone']
    lang = meta['language']

    if intent == "topic_list" and query.lower().startswith(("teach", "let's start", "let us start", "start with", "explain", "i want to learn", "i want to understand")):
        intent = "academic"

    if intent == "academic":
        update_session_topic(session_id, topic="UGC NET")
    elif intent == "emotional":
        set_last_mood(session_id, "emotional")

    if intent == "quiz_start":
        topic = query.split(" on ")[-1] if " on " in query else "UGC NET"
        questions = generate_quiz_questions(topic)
        if not questions or len(questions) < 5:
            return {"response": "Sorry, couldn't generate enough quiz questions right now. Try a different topic?", "session_id": session_id}

        start_quiz(session_id, topic)
        set_active_quiz_topic(session_id, topic)
        quiz_state = get_quiz_state(session_id)
        quiz_state["questions"] = questions
        quiz_state["index"] = 0
        quiz_state["score"] = 0
        quiz_state["answers"] = []
        update_quiz_state(session_id, quiz_state)

        q = questions[0]
        text = f"🎯 Let's begin your quiz on {topic}!\n\nQ1: {q['question']}\nA) {q['A']}\nB) {q['B']}\nC) {q['C']}\nD) {q['D']}"
        return {"response": text, "session_id": session_id}

    elif intent == "quiz_answer":
        quiz = get_quiz_state(session_id)
        if not quiz or "questions" not in quiz:
            return {"response": "Hmm, there's no quiz running right now. Want to start one?", "session_id": session_id}

        idx = quiz.get("index", 0)
        if idx >= len(quiz["questions"]):
            return {"response": "Looks like the quiz is already complete. Want to review it?", "session_id": session_id}

        answer = query.strip().upper().replace(".", "")
        current = quiz["questions"][idx]
        correct = current["answer"]
        is_correct = answer == correct

        quiz.setdefault("answers", []).append({
            "question": current["question"],
            "user_answer": answer,
            "correct_answer": correct,
            "is_correct": is_correct
        })
        if is_correct:
            quiz["score"] += 1
            feedback = "✅ Correct! Nicely done."
        else:
            feedback = f"❌ Oops! The correct answer was {correct}."

        quiz["index"] += 1
        update_quiz_state(session_id, quiz)

        if quiz["index"] >= len(quiz["questions"]):
            score = quiz["score"]
            total = len(quiz["questions"])
            reset_quiz(session_id)
            return {"response": f"{feedback}\n\n🎉 Quiz complete! Your score: {score}/{total}.", "session_id": session_id}

        next_q = quiz["questions"][quiz["index"]]
        text = f"{feedback}\n\n➡️ Next one:\nQ{quiz['index']+1}: {next_q['question']}\nA) {next_q['A']}\nB) {next_q['B']}\nC) {next_q['C']}\nD) {next_q['D']}"
        return {"response": text, "session_id": session_id}

    elif intent == "quiz_continue":
        quiz = get_quiz_state(session_id)
        if not quiz or "questions" not in quiz or quiz.get("index", 0) >= len(quiz["questions"]):
            return {"response": "There's no quiz in progress. Want me to start a new one?", "session_id": session_id}

        q = quiz["questions"][quiz["index"]]
        return {
            "response": f"🟢 Continuing...\nQ{quiz['index']+1}: {q['question']}\nA) {q['A']}\nB) {q['B']}\nC) {q['C']}\nD) {q['D']}",
            "session_id": session_id
        }

    elif intent == "quiz_review":
        quiz = get_quiz_state(session_id)
        if not quiz or "answers" not in quiz:
            return {"response": "No quiz to review yet.", "session_id": session_id}

        answers = quiz["answers"]
        correct = sum(1 for a in answers if a["is_correct"])
        missed = [a["question"] for a in answers if not a["is_correct"]]

        msg = f"📊 You got {correct}/{len(answers)} correct.\n"
        if missed:
            msg += "You struggled with:\n- " + "\n- ".join(missed[:2]) + "\nWant to retry those or review the topic?"
        else:
            msg += "Perfect score! 🏆 Want to try another topic?"

        return {"response": msg, "session_id": session_id}

    elif intent == "topic_list":
        topic = query.lower()
        if "communication" in topic:
            msg = (
                "🗣️ Important topics in Communication:\n"
                "1. Verbal & Non-Verbal Communication\n"
                "2. Barriers to Communication\n"
                "3. Classroom Communication\n"
                "4. Mass Communication\n"
                "5. Interpersonal Skills\n\n"
                "Want to go deeper into one of these?"
            )
        elif "teaching" in topic:
            msg = (
                "📘 Teaching Aptitude Topics:\n"
                "1. Characteristics of Teachers\n"
                "2. Teaching Methods\n"
                "3. Learner Attributes\n"
                "4. Classroom Management\n"
                "5. Evaluation Techniques\n\n"
                "Let me know which one you'd like to explore."
            )
        else:
            msg = "Which subject's topic list do you want? E.g. 'Communication', 'Research Aptitude'?"

        return {"response": msg, "session_id": session_id}

    if intent in ["source_query", "privacy_query", "creator_query"]:
        res = handle_professional_query(intent, query)
        return {"response": res, "session_id": session_id}

    chat_history = get_chat_history_by_session(session_id)
    context = [{"q": c["question_text"], "a": c["response_text"]} for c in chat_history if c.get("response_text")]

    # ✅ NEW: Get relevant vector search context
    vector_context = query_vector_store(query_text=query, user_id=user_id)
    print("🧠 Retrieved Vector Context:", vector_context)

    # ✅ NEW: Inject into prompt
    prompt = build_prompt(
        query,
        history=context,
        context=vector_context,
        session_id=session_id,
        user_id=user_id,
        intent=intent,
        tone=tone,
        language=lang
    )

    raw = get_response_from_llm(prompt)
    final = clean_response(raw)

    save_chat(
        user_id=user_id,
        session_id=session_id,
        subject="UGC NET",
        unit=None,
        topic=None,
        sub_topic=None,
        question_text=query,
        response_text=final,
        source_ref_type="chat",
        intent=intent,
        is_professional=False
    )

    print("prompt:", prompt)
    print("raw:", raw)
    print("final:", final)

    return {"response": final, "session_id": session_id}
