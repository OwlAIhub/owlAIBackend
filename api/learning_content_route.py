from fastapi import APIRouter, HTTPException
from database.learning_content import create_learning_content, get_all_learning_content, update_learning_content, delete_learning_content
from pydantic import BaseModel
from typing import List, Optional

router = APIRouter()

class ContentCreateRequest(BaseModel):
    title: str
    subject: str
    unit: str
    topic: str
    sub_topic: Optional[str] = None
    content_type: str
    content_body: str
    tags: Optional[List[str]] = []

class ContentUpdateRequest(BaseModel):
    title: Optional[str]
    content_type: Optional[str]
    content_body: Optional[str]
    tags: Optional[List[str]]

@router.post("/create")
def create_content_api(req: ContentCreateRequest):
    try:
        content_id = create_learning_content(
            req.title,
            req.subject,
            req.unit,
            req.topic,
            req.sub_topic,
            req.content_type,
            req.content_body,
            req.tags
        )
        return {"status": "success", "content_id": content_id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/")
def get_all_content_api():
    try:
        content = get_all_learning_content()
        return {"status": "success", "data": content}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.patch("/{content_id}/update")
def update_content_api(content_id: str, req: ContentUpdateRequest):
    try:
        update_learning_content(content_id, req.dict(exclude_none=True))
        return {"status": "updated"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{content_id}")
def delete_content_api(content_id: str):
    try:
        delete_learning_content(content_id)
        return {"status": "deleted"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))