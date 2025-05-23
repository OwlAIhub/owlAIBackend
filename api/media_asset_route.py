from fastapi import APIRouter, HTTPException
from database.media_asset import create_media_asset, get_all_media_assets, update_media_asset, delete_media_asset
from pydantic import BaseModel
from typing import List, Optional

router = APIRouter()

class MediaAssetCreateRequest(BaseModel):
    media_type: str
    description: str
    tags: Optional[List[str]] = []
    topic_id: str
    subject: str
    uploaded_by: str
    file_size_kb: int
    resolution: str

class MediaAssetUpdateRequest(BaseModel):
    description: Optional[str]
    tags: Optional[List[str]]
    file_size_kb: Optional[int]
    resolution: Optional[str]

@router.post("/create")
def create_asset_api(req: MediaAssetCreateRequest):
    try:
        media_id = create_media_asset(
            req.media_type,
            req.description,
            req.tags,
            req.topic_id,
            req.subject,
            req.uploaded_by,
            req.file_size_kb,
            req.resolution
        )
        return {"status": "success", "media_id": media_id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/")
def get_assets_api():
    try:
        assets = get_all_media_assets()
        return {"status": "success", "data": assets}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.patch("/{media_id}/update")
def update_asset_api(media_id: str, req: MediaAssetUpdateRequest):
    try:
        update_media_asset(media_id, req.dict(exclude_none=True))
        return {"status": "updated"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{media_id}")
def delete_asset_api(media_id: str):
    try:
        delete_media_asset(media_id)
        return {"status": "deleted"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
