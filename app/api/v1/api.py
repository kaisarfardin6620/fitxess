from fastapi import APIRouter
from app.api.v1.endpoints import generation, onboarding, scanning, tracking

api_router = APIRouter()
api_router.include_router(onboarding.router, prefix="/onboarding", tags=["Onboarding"])
api_router.include_router(generation.router, tags=["AI Generation"])
api_router.include_router(scanning.router, prefix="/scan", tags=["Scanning"])
api_router.include_router(tracking.router, prefix="/tracking", tags=["Tracking"])