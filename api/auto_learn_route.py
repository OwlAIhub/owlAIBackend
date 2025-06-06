from fastapi import APIRouter, HTTPException
from services.auto_learn import retry_failed_answer

router = APIRouter()

@router.post("/retry/{chat_id}")
def regenerate_failed_response(chat_id: str):
    try:
        new_response = retry_failed_answer(chat_id)
        return {"status": "updated", "new_response": new_response}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
