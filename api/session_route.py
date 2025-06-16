from fastapi import APIRouter, HTTPException
from database.sessions import create_session, update_session, end_session
from pydantic import BaseModel
from typing import Optional
import uuid

router = APIRouter()

# Create
@router.post("/create")
def create_session_api(user_id: str):
    session_id = create_session(user_id)
    return {"session_id": session_id}

# Update title or other metadata
class SessionUpdateRequest(BaseModel):
    title: Optional[str] = None
    device_type: Optional[str] = None

@router.patch("/{session_id}")
def update_session_api(session_id: str, req: SessionUpdateRequest):
    try:
        update_session(session_id, req.dict(exclude_none=True))
        return {"status": "updated"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# End (soft delete)
@router.post("/{session_id}/end")
def end_session_api(session_id: str):
    try:
        end_session(session_id)
        return {"status": "ended"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/init-anon")
def init_anonymous_session():
    anon_user_id = f"anon_{uuid.uuid4().hex[:8]}"
    session_id = create_session(anon_user_id, is_anonymous=True)
    return {
        "user_id": anon_user_id,
        "session_id": session_id
    }
