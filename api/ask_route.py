# routes/ask_route.py

from fastapi import APIRouter
from pydantic import BaseModel

from services.llm import (
    build_prompt,
    get_response_from_llm,
    generate_followup_prompt,
    generate_session_summary,
    generate_quiz_questions,
    generate_quiz_step_response
)

from services.session_memory import (
    get_learning_state,
    update_learning_state,
    add_to_history,
    save_quiz_session,
    get_quiz_session,
    clear_quiz_session
)

from services.intent_tone_classifier import classify_intent_language_topic
from services.moderation import run_moderation_check
from services.quiz_manager import QuizSession

ask_router = APIRouter()


class AskRequest(BaseModel):
    session_id: str
    query: str
    user_id: str


@ask_router.post("")
@ask_router.post("/")
async def ask_question(request: AskRequest):
    session_id = request.session_id.strip()
    query = request.query.strip()
    user_id = request.user_id.strip()

    # 🚫 Step 0: Moderation
    mod_result = run_moderation_check(query)
    if mod_result:
        return {"response": mod_result}

    # 🔍 Step 1: Classify query
    meta = classify_intent_language_topic(query)
    intent = meta.get("intent", "concept_explanation")
    language = meta.get("language", "HINGLISH")
    topic = meta.get("topic", "UGC NET")

    # 📘 Step 2: Session learning state
    state = get_learning_state(session_id)
    
    print("🧠 Current Learning State:")
    print(get_learning_state(session_id))


    # 🎯 Reset state if topic changed
    if topic != state["current_unit"]:
        update_learning_state(session_id, {
            "current_unit": topic,
            "current_subtopic": "Introduction",
            "learning_stage": "explanation",
            "has_done_quiz": False,
            "last_question_type": "None"
        })
        state = get_learning_state(session_id)

    # 📝 Step 3: Summary shortcut
    if intent == "summary_request":
        return {"response": generate_session_summary(session_id)}

    # 💬 Step 4: Emotion / Greeting / Off-topic
    if intent in ["emotion", "greeting", "off-topic"]:
        prompt = build_prompt(query, intent, language, session_id, user_id)
        response = get_response_from_llm(prompt)
        add_to_history(session_id, {"query": query, "response": response})
        return {"response": response}

    # 🧪 Step 5: Quiz Answer Handling
    if intent == "quiz_answer":
        quiz_state = get_quiz_session(session_id)
        if quiz_state:
            quiz = QuizSession(topic=quiz_state["topic"], num_questions=quiz_state["num_questions"])
            quiz.questions = quiz_state["questions"]
            quiz.current_index = quiz_state["current_index"]
            quiz.score = quiz_state["score"]
            quiz.answers = quiz_state.get("answers", [])

            user_answer = query.strip().upper()
            quiz.answer_question(user_answer)

            save_quiz_session(session_id, quiz.__dict__)
            if quiz.is_finished():
                clear_quiz_session(session_id)
                update_learning_state(session_id, {"has_done_quiz": True, "learning_stage": "review"})

            quiz_response = generate_quiz_step_response(
                user_answer=user_answer,
                quiz_state=quiz.__dict__,
                tone="friendly",  # fixed tone
                language=language
            )
            return {"response": quiz_response}

    # 📚 Step 6: Teaching / Explanation
    if intent in ["chapter_teaching", "concept_explanation"]:
        prompt = build_prompt(query, intent, language, session_id, user_id)
        response = get_response_from_llm(prompt)

        # Update learning stage
        update_learning_state(session_id, {
    "current_unit": topic,
    "current_subtopic": topic,  # Simplified assumption unless subtopic classifier is added
    "learning_stage": "explanation",
    "has_done_quiz": False
})

        # Suggest follow-up action
        followup = generate_followup_prompt(session_id)
        response += f"\n\n👣 {followup}"

        add_to_history(session_id, {"query": query, "response": response})
        return {"response": response}

    # ❓ Step 7: Quiz Request
    if intent == "quiz_request":
        questions = generate_quiz_questions(state["current_unit"])
        if not questions:
            return {"response": "Sorry, quiz generate nahi ho paaya. Try again later."}

        quiz = QuizSession(topic=state["current_unit"], num_questions=5)
        quiz.add_questions(questions)
        quiz.answers = []
        save_quiz_session(session_id, quiz.__dict__)

        update_learning_state(session_id, {
            "learning_stage": "quiz",
            "has_done_quiz": False
        })

        quiz_response = generate_quiz_step_response(
            user_answer=None,
            quiz_state=quiz.__dict__,
            tone="friendly",
            language=language
        )
        return {"response": quiz_response}

    # 🔚 Fallback: Just build and respond
    prompt = build_prompt(query, intent, language, session_id, user_id)
    response = get_response_from_llm(prompt)
    add_to_history(session_id, {"query": query, "response": response})
    return {"response": response}
