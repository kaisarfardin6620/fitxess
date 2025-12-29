from fastapi import APIRouter
from app.api.v1.endpoints import generation
# import other endpoints here when ready

api_router = APIRouter()
api_router.include_router(generation.router, tags=["AI Generation"])
api_router.include_router(scanning.router, prefix="/scan", tags=["Scanning"])