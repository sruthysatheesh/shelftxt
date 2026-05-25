# backend/routes/recommendations.py

from fastapi import APIRouter
from backend.services.recommendation import get_recommendation

router = APIRouter()


@router.get("/recommend")
async def recommend():
    return get_recommendation()


@router.post("/recommend/refresh")
async def refresh_recommendation():
    get_recommendation.cache_clear()
    return {"status": "recommendation cache cleared"}