from fastapi import APIRouter, HTTPException
from database.chats import save_chat, get_chat_history, delete_chat
from pydantic import BaseModel
from typing import Optional

router = APIRouter()

class ChatCreateRequest(BaseModel):
    session_id: str
    user_id: str
    user_message: str
    bot_response: str
    message_type: Optional[str] = "text"
    timestamp: Optional[str] = None

@router.post("/create")
def create_chat_api(req: ChatCreateRequest):
    try:
        chat_id = save_chat(
            req.session_id,
            req.user_id,
            req.user_message,
            req.bot_response,
            req.message_type,
            req.timestamp
        )
        return {"status": "success", "chat_id": chat_id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{session_id}")
def get_chat_history_api(session_id: str):
    try:
        history = get_chat_history(session_id)
        return {"status": "success", "data": history}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/{chat_id}")
def delete_chat_api(chat_id: str):
    try:
        delete_chat(chat_id)
        return {"status": "deleted"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
