# api/ask_route.py

from fastapi import APIRouter
from pydantic import BaseModel
from services.llm import build_prompt, get_response_from_llm, clean_llm_response
from services.vector_search import query_vector_store

ask_router = APIRouter()

class AskRequest(BaseModel):
    query: str

@ask_router.post("/")
async def ask_question(request: AskRequest):
    """
    Handles POST /ask with a user's query.
    Retrieves context from vector DB and sends prompt to LLM.
    Returns clean, helpful answer.
    """
    query = request.query.strip()

    try:
        # Step 1: Get top 5 context documents from Pinecone
        context_chunks = query_vector_store(query)[:5]

        if not context_chunks:
            return {"response": "No relevant context found in Pinecone."}

        # Step 2: Build prompt with context
        prompt = build_prompt(query, context_chunks)

        # Step 3: Send to Gemini and get response
        raw_answer = get_response_from_llm(prompt)

        # Step 4: Clean the raw Gemini response
        answer = clean_llm_response(raw_answer)

        return {"response": answer}

    except Exception as e:
        return {"error": f"Server error: {str(e)}"}
