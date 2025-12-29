from pydantic import BaseModel
from typing import Optional

class FoodScanResult(BaseModel):
    name: str
    calories: int
    protein: float
    carbs: float
    fats: float
    health_score: int # 1-10 (10 is best)
    warnings: list[str] = [] # ["High Sodium", "Added Sugar"]