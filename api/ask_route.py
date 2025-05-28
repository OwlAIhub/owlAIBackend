# app/routes/ask_route.py

from fastapi import APIRouter
from pydantic import BaseModel
from services.llm import build_prompt, get_response_from_llm
from services.vector_search import query_vector_store

ask_router = APIRouter()

class AskRequest(BaseModel):
    query: str

@ask_router.post("/")  # POST /ask/
async def ask_question(request: AskRequest):
    query = request.query.strip()

    try:
        # Step 1: RAG - Get relevant chunks from Pinecone
        documents = query_vector_store(query, top_k=5)

        if not documents:
            return {"response": "No relevant context found in Pinecone."}

        # Step 2: Build Gemini prompt with context
        prompt = build_prompt(query, documents)

        # Step 3: Call Gemini API with prompt
        answer = get_response_from_llm(prompt)

        return {"response": answer}

    except Exception as e:
        return {"error": f" Server error: {str(e)}"}
