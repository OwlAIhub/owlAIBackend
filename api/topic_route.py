from fastapi import APIRouter, HTTPException
from database.topics import create_topic, get_topics_by_subject, update_topic, delete_topic
from pydantic import BaseModel
from typing import Optional

router = APIRouter()

class TopicCreateRequest(BaseModel):
    subject_id: str
    unit: str
    name: str
    description: Optional[str] = None

class TopicUpdateRequest(BaseModel):
    name: Optional[str]
    unit: Optional[str]
    description: Optional[str]

@router.post("/create")
def create_topic_api(req: TopicCreateRequest):
    try:
        topic_id = create_topic(req.subject_id, req.unit, req.name, req.description)
        return {"status": "success", "topic_id": topic_id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{subject_id}")
def get_topics_api(subject_id: str):
    try:
        topics = get_topics_by_subject(subject_id)
        return {"status": "success", "data": topics}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.patch("/{topic_id}/update")
def update_topic_api(topic_id: str, req: TopicUpdateRequest):
    try:
        update_topic(topic_id, req.dict(exclude_none=True))
        return {"status": "updated"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{topic_id}")
def delete_topic_api(topic_id: str):
    try:
        delete_topic(topic_id)
        return {"status": "deleted"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
