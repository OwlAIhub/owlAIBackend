from fastapi import APIRouter, HTTPException
from database.user_activity import create_user_activity, get_all_user_activities, update_user_activity, delete_user_activity
from pydantic import BaseModel
from typing import List, Optional

router = APIRouter()

class ActivityCreateRequest(BaseModel):
    session_id: str
    user_id: str
    question_log: str
    confusion_flag: Optional[bool] = False
    auto_generated_tags: Optional[List[str]] = []
    language_pattern: Optional[str] = None
    session_duration: Optional[int] = 0

class ActivityUpdateRequest(BaseModel):
    session_duration: Optional[int]
    language_pattern: Optional[str]

@router.post("/create")
def create_activity_api(req: ActivityCreateRequest):
    try:
        activity_id = create_user_activity(
            req.session_id,
            req.user_id,
            req.question_log,
            req.confusion_flag,
            req.auto_generated_tags,
            req.language_pattern,
            req.session_duration
        )
        return {"status": "success", "activity_id": activity_id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/")
def get_activities_api():
    try:
        activities = get_all_user_activities()
        return {"status": "success", "data": activities}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.patch("/{activity_id}/update")
def update_activity_api(activity_id: str, req: ActivityUpdateRequest):
    try:
        update_user_activity(activity_id, req.dict(exclude_none=True))
        return {"status": "updated"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{activity_id}")
def delete_activity_api(activity_id: str):
    try:
        delete_user_activity(activity_id)
        return {"status": "deleted"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
