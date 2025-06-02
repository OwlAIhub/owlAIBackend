# api/ask_route.py

from fastapi import APIRouter
from pydantic import BaseModel
from services.llm import build_prompt, get_response_from_llm, clean_llm_response
from services.vector_search import query_vector_store
from database.chats import save_chat, get_chat_history
from services.moderation import run_moderation_check
from services.intent_classifier import classify_intent

ask_router = APIRouter()

class AskRequest(BaseModel):
    query: str
    user_id: str


@ask_router.post("")
@ask_router.post("/")
async def ask_question(request: AskRequest):
    query = request.query.strip()
    user_id = request.user_id.strip()

    # 🔹 Step 1: Run moderation first
    override_response = run_moderation_check(query)
    if override_response:
        return {"response": override_response}

    # 🔹 Step 2: Classify intent
    intent = classify_intent(query)

    try:
        # Step 3: Fetch DB context
        raw_chunks = query_vector_store(query, user_id=user_id)
        context_chunks = raw_chunks[:5] if raw_chunks else []

        # Step 4: Past 3 Q&As
        history_chunks = []
        chat_docs = get_chat_history(user_id)
        for doc in chat_docs[-3:]:
            q = doc.get("question_text", "")
            a = doc.get("response_text", "")
            history_chunks.append(f"Q: {q}\nA: {a}")

        # Step 5: Combine all context
        combined_context = [{"metadata": {"text": h}} for h in history_chunks] + \
                           [{"metadata": {"text": c["text"]}} for c in context_chunks]

        # Step 6: Prompt + response
        prompt = build_prompt(query, combined_context, user_id=user_id, intent_tag=intent)
        raw_answer = get_response_from_llm(prompt)
        answer = clean_llm_response(raw_answer)

        # Step 7: Save result
        save_chat(
            user_id=user_id,
            subject="UGC NET",
            unit=None,
            topic=None,
            sub_topic=None,
            question_text=query,
            response_text=answer,
            source_ref_type="rag",
        )

        return {"response": answer}

    except Exception as e:
        return {"error": f"Server error: {str(e)}"}