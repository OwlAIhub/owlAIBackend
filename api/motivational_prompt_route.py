from fastapi import APIRouter, HTTPException
from database.motivational_prompts import create_motivational_prompt, get_all_prompts, update_prompt, delete_prompt
from pydantic import BaseModel
from typing import List, Optional

router = APIRouter()

class PromptCreateRequest(BaseModel):
    text: str
    stage_trigger: str
    user_type_tags: Optional[List[str]] = []
    visual_type: str
    delivery_time: str
    target_emotion: str
    delivery_channel: str

class PromptUpdateRequest(BaseModel):
    text: Optional[str]
    target_emotion: Optional[str]
    visual_type: Optional[str]

@router.post("/create")
def create_prompt_api(req: PromptCreateRequest):
    try:
        prompt_id = create_motivational_prompt(
            req.text,
            req.stage_trigger,
            req.user_type_tags,
            req.visual_type,
            req.delivery_time,
            req.target_emotion,
            req.delivery_channel
        )
        return {"status": "success", "prompt_id": prompt_id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/")
def get_prompts_api():
    try:
        prompts = get_all_prompts()
        return {"status": "success", "data": prompts}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.patch("/{prompt_id}/update")
def update_prompt_api(prompt_id: str, req: PromptUpdateRequest):
    try:
        update_prompt(prompt_id, req.dict(exclude_none=True))
        return {"status": "updated"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{prompt_id}")
def delete_prompt_api(prompt_id: str):
    try:
        delete_prompt(prompt_id)
        return {"status": "deleted"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
