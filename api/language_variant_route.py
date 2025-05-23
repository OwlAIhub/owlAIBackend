from fastapi import APIRouter, HTTPException
from database.language_variants import create_language_variant, get_all_language_variants, update_language_variant, delete_language_variant
from pydantic import BaseModel
from typing import Optional

router = APIRouter()

class VariantCreateRequest(BaseModel):
    subject: str
    unit: str
    topic: str
    original_text: str
    translated_text: str
    language: str
    tone_type: str

class VariantUpdateRequest(BaseModel):
    translated_text: Optional[str]
    tone_type: Optional[str]

@router.post("/create")
def create_variant_api(req: VariantCreateRequest):
    try:
        variant_id = create_language_variant(
            req.subject,
            req.unit,
            req.topic,
            req.original_text,
            req.translated_text,
            req.language,
            req.tone_type
        )
        return {"status": "success", "variant_id": variant_id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/")
def get_variants_api():
    try:
        variants = get_all_language_variants()
        return {"status": "success", "data": variants}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.patch("/{variant_id}/update")
def update_variant_api(variant_id: str, req: VariantUpdateRequest):
    try:
        update_language_variant(variant_id, req.dict(exclude_none=True))
        return {"status": "updated"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{variant_id}")
def delete_variant_api(variant_id: str):
    try:
        delete_language_variant(variant_id)
        return {"status": "deleted"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
