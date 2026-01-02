from pydantic import BaseModel
from typing import Optional

class FoodScanResult(BaseModel):
    name: str
    calories: int
    protein: float
    carbs: float
    fats: float
    health_score: int
    warnings: list[str] = []