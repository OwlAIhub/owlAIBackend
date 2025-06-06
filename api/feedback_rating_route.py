from fastapi import APIRouter, HTTPException
<<<<<<< HEAD
from database.feedback_rating import create_feedback, get_feedback_by_chat, update_feedback, delete_feedback, get_flagged_chats
=======
from database.feedback_rating import create_feedback, get_feedback_by_chat, update_feedback, delete_feedback
>>>>>>> 2d81c63860a1cdaa3570f84e871396f242228972
from pydantic import BaseModel
from typing import Optional

router = APIRouter()

class FeedbackCreateRequest(BaseModel):
    chat_id: str
<<<<<<< HEAD
    user_id: str
    usefulness_score: int  # like = 1, dislike = 0
    content_quality_score: int
    flagged_reason: Optional[str] = None
    remarks: Optional[str] = None

=======
    rating: int
    comment: Optional[str] = None
>>>>>>> 2d81c63860a1cdaa3570f84e871396f242228972

class FeedbackUpdateRequest(BaseModel):
    rating: Optional[int]
    comment: Optional[str]

@router.post("/create")
def create_feedback_api(req: FeedbackCreateRequest):
    try:
<<<<<<< HEAD
        feedback_id = create_feedback(
            req.chat_id,
            req.user_id,
            req.usefulness_score,
            req.content_quality_score,
            req.flagged_reason,
            req.remarks
        )
=======
        feedback_id = create_feedback(req.chat_id, req.rating, req.comment)
>>>>>>> 2d81c63860a1cdaa3570f84e871396f242228972
        return {"status": "success", "feedback_id": feedback_id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

<<<<<<< HEAD

=======
>>>>>>> 2d81c63860a1cdaa3570f84e871396f242228972
@router.get("/{chat_id}")
def get_feedback_api(chat_id: str):
    try:
        feedback = get_feedback_by_chat(chat_id)
        return {"status": "success", "data": feedback}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.patch("/{feedback_id}/update")
def update_feedback_api(feedback_id: str, req: FeedbackUpdateRequest):
    try:
        update_feedback(feedback_id, req.dict(exclude_none=True))
        return {"status": "updated"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{feedback_id}")
def delete_feedback_api(feedback_id: str):
    try:
        delete_feedback(feedback_id)
        return {"status": "deleted"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
<<<<<<< HEAD

@router.get("/flagged")
def get_flagged_chats_api():
    try:
        flagged = get_flagged_chats(min_score=0)
        return {"status": "success", "data": flagged}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

=======
>>>>>>> 2d81c63860a1cdaa3570f84e871396f242228972
