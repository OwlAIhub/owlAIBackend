from fastapi import APIRouter
from pydantic import BaseModel
from database.sessions import create_session
from database.chats import save_chat
from services.llm import (
    build_prompt,
    get_response_from_llm,
    generate_followup_prompt,
    generate_session_summary, generate_chat_title
)
from services.session_memory import (
    set_session_data,
    get_user_name,
    get_session_state
)
from services.intent_tone_classifier import classify_intent_language_topic
from services.moderation import run_moderation_check

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
    name = get_user_name(user_id) if not user_id.startswith("anon_") else ""


    # Detect anonymous user
    is_anon = user_id.startswith("anon_")

    # Create session if new
    if session_id.lower() == "new":
        session_id = create_session(user_id, is_anonymous=is_anon)
        print(f"Created new session: {session_id} for user: {user_id} (anonymous={is_anon})")

    #  Enforce 3-chat limit for anonymous users
    session = get_session_state(session_id)
    is_anon = session.get("is_anonymous", False)
    message_count = session.get("message_count", 0)

    if is_anon and message_count >= 3:
        return {
            "response": "🔐 You’ve reached the guest limit of 3 messages. Please log in to continue learning with OwlAI.",
            "session_id": session_id,
            "chat_id": None
        }

    #  Increment count if allowed
    if is_anon:
        set_session_data(session_id, {"message_count": message_count + 1})

    # Step 0: Moderation
    mod_result = run_moderation_check(query)
    if mod_result:
        return {
            "response": mod_result,
            "session_id": session_id,
            "chat_id": None
        }

    # Step 1: Intent classification
    meta = classify_intent_language_topic(query)
    intent = meta.get("intent", "concept_explanation")
    language = meta.get("language", "HINGLISH")
    topic = meta.get("topic", "UGC NET")

    # Step 2: Save topic
    set_session_data(session_id, {"active_topic": topic})

    # Step 3: Summary request
    if intent == "summary_request":
        summary = generate_session_summary(session_id)
        return {
            "response": summary,
            "session_id": session_id,
            "chat_id": None
        }

    # Step 4: Greetings / Emotion / Off-topic
    if intent in ["greeting", "emotion", "off-topic"]:
        # Step 6
        add_greeting = intent == "greeting" or session.get("message_count", 0) == 0
        prompt = build_prompt(query, intent, language, session_id, user_id, name if add_greeting else None)

        response = get_response_from_llm(prompt)
        title = generate_chat_title(query, response)
        chat_id = save_chat(
            session_id, user_id, "UGC NET", "General Paper", topic, "", query, response,
            source_ref_type="user_input", title=title, intent=intent
        )
        return {
            "response": response,
            "session_id": session_id,
            "chat_id": chat_id
        }

    # Step 5: Explanation or Chapter Teaching
    if intent in ["chapter_teaching", "concept_explanation"]:
        # Step 6
        add_greeting = intent == "greeting" or session.get("message_count", 0) == 0
        prompt = build_prompt(query, intent, language, session_id, user_id, name if add_greeting else None)

        response = get_response_from_llm(prompt)
        followup = generate_followup_prompt(session_id)
        title = generate_chat_title(query, response)
        response += f"\n\n👣 {followup}"
        chat_id = save_chat(
            session_id, user_id, "UGC NET", "General Paper", topic, "", query, response,
            source_ref_type="user_input", title=title, intent=intent
        )

        session_meta = get_session_state(session_id)
        old_title = session_meta.get("title", "")
        if not old_title or old_title.lower().startswith("hi") or len(old_title) < 10:
            set_session_data(session_id, {"title": title})

        session_history = session.get("history", [])
        session_history.append({"query": query, "response": response})
        set_session_data(session_id, {"history": session_history})

        
        return {
            "response": response,
            "session_id": session_id,
            "chat_id": chat_id
        }

    # Step 6: Fallback# Step 6
    add_greeting = intent == "greeting" or session.get("message_count", 0) == 0
    prompt = build_prompt(query, intent, language, session_id, user_id, name if add_greeting else None)

    response = get_response_from_llm(prompt)
    title = generate_chat_title(query, response)
    chat_id = save_chat(
        session_id, user_id, "UGC NET", "General Paper", topic, "", query, response,
        source_ref_type="user_input", title=title, intent=intent
    )
    session_meta = get_session_state(session_id)
    session_history = session.get("history", [])
    session_history.append({"query": query, "response": response})
    set_session_data(session_id, {"history": session_history, "title": title})


    return {
        "response": response,
        "session_id": session_id,
        "chat_id": chat_id
    }
