# routes/ask_route.py

from fastapi import APIRouter
from pydantic import BaseModel

from services.intent_tone_classifier import classify_intent_tone_language
from services.llm import build_prompt, get_response_from_llm
from services.session_memory import add_to_history
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

    # 🚫 Moderation check
    mod_result = run_moderation_check(query)
    if mod_result:
        return {"response": mod_result}

    # 🔍 Step 1: Classify
    meta = classify_intent_tone_language(query)
    intent = meta.get("intent", "concept_explanation")
    tone = meta.get("tone", "neutral")
    language = meta.get("language", "ENGLISH")

    # 🧠 Step 2: Build prompt
    prompt = build_prompt(query, intent, tone, language, session_id, user_id)

    # 🤖 Step 3: Get GPT response
    response = get_response_from_llm(prompt)

    # 🧾 Step 4: Save to history
    add_to_history(session_id, {"user": query, "bot": response})

    # ✅ Step 5: Return
    return {"response": response}
