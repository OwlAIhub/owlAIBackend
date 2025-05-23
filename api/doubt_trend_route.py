from fastapi import APIRouter, HTTPException
from database.doubt_trend import create_doubt_trend, get_all_doubt_trends, update_doubt_trend, delete_doubt_trend
from pydantic import BaseModel
from typing import List, Optional

router = APIRouter()

class DoubtTrendCreateRequest(BaseModel):
    title: str
    subject: str
    unit: str
    topic: str
    sub_topic: Optional[str] = None
    question_ids: Optional[List[str]] = []
    frequency_count: Optional[List[int]] = []
    trending_score: int
    date_range: Optional[str] = None
    geo_location: Optional[str] = None

class DoubtTrendUpdateRequest(BaseModel):
    title: Optional[str]
    frequency_count: Optional[List[int]]
    trending_score: Optional[int]
    geo_location: Optional[str]

@router.post("/create")
def create_trend_api(req: DoubtTrendCreateRequest):
    try:
        feed_id = create_doubt_trend(
            req.title,
            req.subject,
            req.unit,
            req.topic,
            req.sub_topic,
            req.question_ids,
            req.frequency_count,
            req.trending_score,
            req.date_range,
            req.geo_location
        )
        return {"status": "success", "feed_id": feed_id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/")
def get_trends_api():
    try:
        trends = get_all_doubt_trends()
        return {"status": "success", "data": trends}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.patch("/{feed_id}/update")
def update_trend_api(feed_id: str, req: DoubtTrendUpdateRequest):
    try:
        update_doubt_trend(feed_id, req.dict(exclude_none=True))
        return {"status": "updated"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{feed_id}")
def delete_trend_api(feed_id: str):
    try:
        delete_doubt_trend(feed_id)
        return {"status": "deleted"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
