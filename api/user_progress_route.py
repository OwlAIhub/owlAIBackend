from fastapi import APIRouter, HTTPException
from database.user_progress import create_or_update_user_progress, get_user_progress, delete_user_progress
from pydantic import BaseModel
from typing import List, Dict, Optional

router = APIRouter()

class ProgressCreateRequest(BaseModel):
    user_id: str
    topic_id: str
    completion_percentage: float
    confidence_level: float
    repeated_doubt_ids: Optional[List[str]] = []
    assessment_scores: Optional[Dict[str, float]] = {}
    time_spent_minutes: int

@router.post("/create_or_update")
def create_or_update_progress(req: ProgressCreateRequest):
    try:
        create_or_update_user_progress(
            req.user_id,
            req.topic_id,
            req.completion_percentage,
            req.confidence_level,
            req.repeated_doubt_ids,
            req.assessment_scores,
            req.time_spent_minutes
        )
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{user_id}")
def get_user_progress_api(user_id: str):
    try:
        progress = get_user_progress(user_id)
        return {"status": "success", "data": progress}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/{user_id}/{topic_id}")
def delete_user_progress_api(user_id: str, topic_id: str):
    try:
        delete_user_progress(user_id, topic_id)
        return {"status": "deleted"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
