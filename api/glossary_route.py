from fastapi import APIRouter, HTTPException
from database.glossary import create_glossary_term, get_glossary_terms, update_glossary_term, delete_glossary_term
from pydantic import BaseModel
from typing import Optional

router = APIRouter()

class GlossaryCreateRequest(BaseModel):
    term: str
    definition: str
    subject: Optional[str] = None
    topic: Optional[str] = None

class GlossaryUpdateRequest(BaseModel):
    term: Optional[str]
    definition: Optional[str]
    subject: Optional[str]
    topic: Optional[str]

@router.post("/create")
def create_term_api(req: GlossaryCreateRequest):
    try:
        term_id = create_glossary_term(req.term, req.definition, req.subject, req.topic)
        return {"status": "success", "term_id": term_id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/")
def get_all_terms_api():
    try:
        terms = get_glossary_terms()
        return {"status": "success", "data": terms}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.patch("/{term_id}/update")
def update_term_api(term_id: str, req: GlossaryUpdateRequest):
    try:
        update_glossary_term(term_id, req.dict(exclude_none=True))
        return {"status": "updated"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{term_id}")
def delete_term_api(term_id: str):
    try:
        delete_glossary_term(term_id)
        return {"status": "deleted"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
