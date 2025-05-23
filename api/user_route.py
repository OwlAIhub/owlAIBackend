from fastapi import APIRouter, HTTPException
from database.user import create_user, get_user, update_user, delete_user
from pydantic import BaseModel
from typing import List, Optional

router = APIRouter()

# Request schemas
class UserCreateRequest(BaseModel):
    name: str
    email: str
    phone: Optional[str] = None
    exam_ids: List[str]
    region: Optional[str] = None
    referral_code: Optional[str] = None

class UserUpdateRequest(BaseModel):
    name: Optional[str]
    phone: Optional[str]
    region: Optional[str]

# Routes

@router.post("/create")
def create_user_api(req: UserCreateRequest):
    try:
        user_id = create_user(req.name, req.email, req.phone, req.exam_ids, req.region, req.referral_code)
        return {"status": "success", "user_id": user_id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{user_id}")
def get_user_api(user_id: str):
    try:
        user_data = get_user(user_id)
        return {"status": "success", "data": user_data}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.patch("/{user_id}/update")
def update_user_api(user_id: str, req: UserUpdateRequest):
    try:
        update_user(user_id, req.dict(exclude_none=True))
        return {"status": "updated"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{user_id}")
def delete_user_api(user_id: str):
    try:
        delete_user(user_id)
        return {"status": "deleted"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
