# api/ask_route.py

from fastapi import APIRouter
from pydantic import BaseModel
from services.llm import build_prompt, get_response_from_llm, clean_llm_response
from services.vector_search import query_vector_store
from database.chats import save_chat, get_chat_history

ask_router = APIRouter()

class AskRequest(BaseModel):
    query: str
    user_id: str

@ask_router.post("")
@ask_router.post("/")
async def ask_question(request: AskRequest):
    query = request.query.strip()
    user_id = request.user_id.strip()

    try:
        # Step 1: Query Pinecone vector store with optional user filter
        raw_chunks = query_vector_store(query, user_id=user_id)
        context_chunks = raw_chunks[:5] if raw_chunks else []

        # Step 2: Get user’s last 3 Q&A pairs from Firestore
        history_chunks = []
        chat_docs = get_chat_history(user_id)
        for doc in chat_docs[-3:]:
            q = doc.get("question_text", "")
            a = doc.get("response_text", "")
            history_chunks.append(f"Q: {q}\nA: {a}")

        # Step 3: Merge both into prompt context
        combined_context = [{"metadata": {"text": h}} for h in history_chunks] + \
                           [{"metadata": {"text": c["text"]}} for c in context_chunks]

        # Step 4: Build + query LLM
        prompt = build_prompt(query, combined_context, user_id=user_id)
        raw_answer = get_response_from_llm(prompt)
        answer = clean_llm_response(raw_answer)

        # Step 5: Save to Firestore
        save_chat(
            user_id=user_id,
            subject="UGC NET",
            unit=None,
            topic=None,
            sub_topic=None,
            question_text=query,
            response_text=answer,
            source_ref_type="rag",
            source_ref_id=None
        )

        return {"response": answer}

    except Exception as e:
        return {"error": f"Server error: {str(e)}"}
