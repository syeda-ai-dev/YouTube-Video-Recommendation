from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from backend.retrieve.retrieve import get_recommendation

router = APIRouter()

class RecommendationRequest(BaseModel):
    keyword: str

@router.post("/recommend")
async def recommend_video(request: RecommendationRequest):
    result = get_recommendation(request.keyword)
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    if not result:
        raise HTTPException(status_code=404, detail="No recommendation found")
    return result
