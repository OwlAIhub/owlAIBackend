# api/ask_route.py

from fastapi import APIRouter
from pydantic import BaseModel
from services.llm import build_prompt, get_response_from_llm, clean_llm_response
from services.vector_search import query_vector_store
from database.chats import save_chat, get_chat_history_by_session
from services.moderation import run_moderation_check
from services.intent_classifier import classify_intent
from database.sessions import create_session
from services.session_memory import update_session_topic
from services.llm import extract_topic_via_llm

from services.llm import generate_chat_title
from services.professional_handler import handle_professional_query

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

    if not session_id or session_id.lower() == "new":
        session_id = create_session(user_id)

    # Step 1: Moderation check
    override_response = run_moderation_check(query)
    if override_response:
        return {"response": override_response}

    # Step 2: Intent classification
    intent = classify_intent(query)

    # Step 3: Handle professional queries immediately
    if intent in ["source_query", "privacy_query", "creator_query"]:
        professional_response = handle_professional_query(intent, query)
        chat_id = save_chat(
            user_id=user_id,
            session_id=session_id,
            subject="UGC NET",
            unit=None,
            topic=None,
            sub_topic=None,
            question_text=query,
            response_text=professional_response,
            source_ref_type="professional",
            title=query[:40],
            intent=intent,
            is_professional=True
        )
        return {
            "response": professional_response,
            "session_id": session_id,
            "chat_id": chat_id
        }

    try:
        # Step 4: Context from vector store (for academic-type intents)
        context_chunks = []
        if intent in ["academic", "feedback", "mcq"]:
            raw_chunks = query_vector_store(query, user_id=user_id)
            if isinstance(raw_chunks, list):
                context_chunks = raw_chunks[:5]

        # Step 5: History from this session only
        history_chunks = []
        chat_docs = get_chat_history_by_session(session_id)
        relevant_docs = [doc for doc in reversed(chat_docs) if doc.get("intent") in ["academic", "mcq", "feedback"]]
        for doc in relevant_docs[:3]:
            q = doc.get("question_text", "")
            a = doc.get("response_text", "")
            history_chunks.append(f"Q: {q}\nA: {a}")

        # Step 6: Build prompt and get response
        combined_context = [{"metadata": {"text": h}} for h in history_chunks] + \
                           [{"metadata": {"text": c["text"]}} for c in context_chunks]

        prompt = build_prompt(query, combined_context, user_id=user_id, session_id=session_id, intent_tag=intent)
        raw_answer = get_response_from_llm(prompt, intent_tag=intent)
        answer = clean_llm_response(raw_answer)
        title = generate_chat_title(query, answer)

        # Step 7: Save only academic-type chats
        chat_id = None
        if intent in ["academic", "mcq", "feedback"]:
            extracted_topic = extract_topic_via_llm(query)
            update_session_topic(session_id, topic=extracted_topic, aspect=query)

            chat_id = save_chat(
                user_id=user_id,
                session_id=session_id,
                subject="UGC NET",
                unit=None,
                topic=None,
                sub_topic=None,
                question_text=query,
                response_text=answer,
                source_ref_type="rag",
                title=title,
                intent=intent,
                is_professional=False
            )


        return {
            "response": answer,
            "session_id": session_id,
            "chat_id": chat_id
        }

    except Exception as e:
        chat_id = save_chat(
            user_id=user_id,
            session_id=session_id,
            subject="UGC NET",
            unit=None,
            topic=None,
            sub_topic=None,
            question_text=query,
            response_text=f"Error: {str(e)}",
            source_ref_type="error",
            title="System Error",
            intent="error",
            is_professional=False
        )
        return {
            "error": f"Server error: {str(e)}",
            "session_id": session_id,
            "chat_id": chat_id
        }
