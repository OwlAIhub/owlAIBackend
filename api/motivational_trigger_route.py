from fastapi import APIRouter, HTTPException
from database.motivational_triggers import create_motivational_trigger, get_all_motivational_triggers, update_motivational_trigger, delete_motivational_trigger
from pydantic import BaseModel
from typing import Optional

router = APIRouter()

class TriggerCreateRequest(BaseModel):
    condition_type: str
    trigger_value: int
    message_template: str
    visual_emoji: str
    audience_type: str
    trigger_priority: int
    ab_test_status: Optional[str] = "active"

class TriggerUpdateRequest(BaseModel):
    message_template: Optional[str]
    trigger_priority: Optional[int]
    ab_test_status: Optional[str]

@router.post("/create")
def create_trigger_api(req: TriggerCreateRequest):
    try:
        trigger_id = create_motivational_trigger(
            req.condition_type,
            req.trigger_value,
            req.message_template,
            req.visual_emoji,
            req.audience_type,
            req.trigger_priority,
            req.ab_test_status
        )
        return {"status": "success", "trigger_id": trigger_id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/")
def get_triggers_api():
    try:
        triggers = get_all_motivational_triggers()
        return {"status": "success", "data": triggers}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.patch("/{trigger_id}/update")
def update_trigger_api(trigger_id: str, req: TriggerUpdateRequest):
    try:
        update_motivational_trigger(trigger_id, req.dict(exclude_none=True))
        return {"status": "updated"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{trigger_id}")
def delete_trigger_api(trigger_id: str):
    try:
        delete_motivational_trigger(trigger_id)
        return {"status": "deleted"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
