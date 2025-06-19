from fastapi import APIRouter, HTTPException
from database.user import create_user, get_user, update_user, delete_user, is_mobile_registered
from pydantic import BaseModel
from typing import List, Optional

router = APIRouter()

class UserCreateRequest(BaseModel):
    first_name: str
    last_name: str
    email: str
    mobile_number: Optional[str]
    curriculum: str
    exam_cycle: str
    attempt: str
    language: str
    selected_subjects: List[str]
    exam_ids: List[str]
    submitted_at: str
    heard_from: Optional[str] = None
    other_subject: Optional[str] = None
    gender: Optional[str] = None
    age_group: Optional[str] = None
    region: Optional[str] = None
    referral_code: Optional[str] = None

class UserUpdateRequest(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    mobile_number: Optional[str]
    region: Optional[str]

# Routes
@router.post("/user/create")
def create_user_api(req: UserCreateRequest):
    try:
        if req.mobile_number and is_mobile_registered(req.mobile_number):
            raise HTTPException(status_code=409, detail="Mobile number already registered.")

        user_id = create_user(
            first_name=req.first_name,
            last_name=req.last_name,
            email=req.email,
            mobile_number=req.mobile_number,
            curriculum=req.curriculum,
            exam_cycle=req.exam_cycle,
            attempt=req.attempt,
            language=req.language,
            selected_subjects=req.selected_subjects,
            exam_ids=req.exam_ids,
            submitted_at=req.submitted_at,
            heard_from=req.heard_from,
            other_subject=req.other_subject,
            gender=req.gender,
            age_group=req.age_group,
            region=req.region,
            referral_code=req.referral_code
        )
        return {"status": "success", "user_id": user_id}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/user/{user_id}")
def get_user_api(user_id: str):
    try:
        user_data = get_user(user_id)
        return {"status": "success", "data": user_data}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.patch("/user/{user_id}/update")
def update_user_api(user_id: str, req: UserUpdateRequest):
    try:
        update_user(user_id, req.dict(exclude_none=True))
        return {"status": "updated"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/user/{user_id}")
def delete_user_api(user_id: str):
    try:
        delete_user(user_id)
        return {"status": "deleted"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
