from fastapi import APIRouter, HTTPException
from database.chats import save_chat, get_chat_history, delete_chat
from database.sessions import get_sessions_by_user
from pydantic import BaseModel
from typing import Optional
from database.sessions import rename_session
from database.sessions import delete_session
from database.chats import delete_chats_by_session




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

# 🔹 NEW: Get chat history by user_id (for sidebar history)
@router.get("/history/by-user")
def get_chat_history_by_user(user_id: str):
    try:
        history = get_chat_history(user_id)
        cleaned = [{
            "chat_id": chat.get("chat_id"),
            "title": chat.get("title") or chat.get("question_text", "")[:40],
            "question_text": chat.get("question_text"),
            "response_text": chat.get("response_text"),
            "timestamp": chat.get("timestamp")
        } for chat in history]
        return {"status": "success", "data": cleaned}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch history: {str(e)}")


@router.get("/sidebar/sessions")
def get_sidebar_sessions(user_id: str):
    try:
        sessions = get_sessions_by_user(user_id)
        all_chats = get_chat_history(user_id)

        # Group chats by session
        session_map = {}
        for chat in all_chats:
            sid = chat["session_id"]
            session_map.setdefault(sid, []).append(chat)

        sidebar_data = []
        for session in sessions:
            sid = session["session_id"]
            chats = session_map.get(sid, [])
            if not chats:
                continue
            latest_chat = sorted(chats, key=lambda x: x.get("timestamp", 0))[-1]
            sidebar_data.append({
                "session_id": sid,
                "title": latest_chat.get("title") or latest_chat.get("question_text", "")[:40],
                "num_chats": len(chats),
                "last_updated": latest_chat.get("timestamp"),
                "start_time": session.get("start_time"),
            })

        return {"status": "success", "data": sidebar_data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch sidebar sessions: {str(e)}")
    
class RenameSessionRequest(BaseModel):
    session_id: str
    new_name: str

@router.patch("/session/rename")
def rename_session_api(req: RenameSessionRequest):
    try:
        rename_session(req.session_id, req.new_name)
        return {"status": "success", "message": "Session renamed"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Rename failed: {str(e)}")


@router.delete("/session/{session_id}")
def delete_session_api(session_id: str):
    try:
        delete_chats_by_session(session_id)
        delete_session(session_id)
        return {"status": "success", "message": "Session and its chats deleted"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Delete failed: {str(e)}")
