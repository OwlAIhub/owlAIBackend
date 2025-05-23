from fastapi import APIRouter, HTTPException
from database.ai_training_logs import create_ai_training_log, get_all_ai_training_logs, update_ai_training_log, delete_ai_training_log
from pydantic import BaseModel
from typing import Optional

router = APIRouter()

class LogCreateRequest(BaseModel):
    prompt_text: str
    ai_response: str
    feedback_score: int
    corrected_by_admin: Optional[str] = None
    training_tag: Optional[str] = None
    model_version: Optional[str] = None

class LogUpdateRequest(BaseModel):
    feedback_score: Optional[int]
    training_tag: Optional[str]

@router.post("/create")
def create_log_api(req: LogCreateRequest):
    try:
        log_id = create_ai_training_log(
            req.prompt_text,
            req.ai_response,
            req.feedback_score,
            req.corrected_by_admin,
            req.training_tag,
            req.model_version
        )
        return {"status": "success", "log_id": log_id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/")
def get_logs_api():
    try:
        logs = get_all_ai_training_logs()
        return {"status": "success", "data": logs}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.patch("/{log_id}/update")
def update_log_api(log_id: str, req: LogUpdateRequest):
    try:
        update_ai_training_log(log_id, req.dict(exclude_none=True))
        return {"status": "updated"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{log_id}")
def delete_log_api(log_id: str):
    try:
        delete_ai_training_log(log_id)
        return {"status": "deleted"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
