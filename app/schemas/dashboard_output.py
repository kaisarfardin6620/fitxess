from pydantic import BaseModel
from typing import List, Dict, Any

class MacroTarget(BaseModel):
    protein: int
    carbs: int
    fats: int
    calories: int
    hydration_ml: int

class FunctionalScore(BaseModel):
    category: str 
    score: int    
    description: str

class DashboardResponse(BaseModel):
    user_id: int
    daily_targets: MacroTarget
    micronutrient_targets: Dict[str, float] 
    functional_scores: List[FunctionalScore]
    recommended_foods: List[Dict[str, str]]