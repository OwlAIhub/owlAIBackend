from fastapi import APIRouter, HTTPException
from database.subjects import create_subject, get_subjects, update_subject, delete_subject
from pydantic import BaseModel
from typing import Optional

router = APIRouter()

class SubjectCreateRequest(BaseModel):
    name: str
    description: Optional[str] = None
    exam_ids: Optional[list] = []

class SubjectUpdateRequest(BaseModel):
    name: Optional[str]
    description: Optional[str]
    exam_ids: Optional[list]

@router.post("/create")
def create_subject_api(req: SubjectCreateRequest):
    try:
        subject_id = create_subject(req.name, req.description, req.exam_ids)
        return {"status": "success", "subject_id": subject_id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/")
def get_subjects_api():
    try:
        subjects = get_subjects()
        return {"status": "success", "data": subjects}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.patch("/{subject_id}/update")
def update_subject_api(subject_id: str, req: SubjectUpdateRequest):
    try:
        update_subject(subject_id, req.dict(exclude_none=True))
        return {"status": "updated"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{subject_id}")
def delete_subject_api(subject_id: str):
    try:
        delete_subject(subject_id)
        return {"status": "deleted"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
