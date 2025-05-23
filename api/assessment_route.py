from fastapi import APIRouter, HTTPException
from database.assessment import create_assessment, get_all_assessments, update_assessment, delete_assessment
from pydantic import BaseModel
from typing import List, Optional

router = APIRouter()

class AssessmentCreateRequest(BaseModel):
    subject: str
    unit: str
    assessment_type: str
    difficulty_level: str
    content_ids: List[str]
    duration_minutes: int
    passing_score: int

class AssessmentUpdateRequest(BaseModel):
    duration_minutes: Optional[int]
    passing_score: Optional[int]

@router.post("/create")
def create_assessment_api(req: AssessmentCreateRequest):
    try:
        assessment_id = create_assessment(
            req.subject,
            req.unit,
            req.assessment_type,
            req.difficulty_level,
            req.content_ids,
            req.duration_minutes,
            req.passing_score
        )
        return {"status": "success", "assessment_id": assessment_id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/")
def get_assessments_api():
    try:
        assessments = get_all_assessments()
        return {"status": "success", "data": assessments}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.patch("/{assessment_id}/update")
def update_assessment_api(assessment_id: str, req: AssessmentUpdateRequest):
    try:
        update_assessment(assessment_id, req.dict(exclude_none=True))
        return {"status": "updated"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{assessment_id}")
def delete_assessment_api(assessment_id: str):
    try:
        delete_assessment(assessment_id)
        return {"status": "deleted"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
