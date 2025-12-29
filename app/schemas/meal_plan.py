# app/schemas/meal_plan.py
from pydantic import BaseModel
from typing import List, Dict, Optional

class MealItem(BaseModel):
    name: str
    calories: int
    protein: float
    carbs: float
    fats: float
    image_url: Optional[str] = None

class DailyMealPlan(BaseModel):
    day: str  # "Monday"
    total_calories: int
    meals: Dict[str, MealItem]  # {"breakfast": {...}, "lunch": {...}}

class WeeklyMealPlanResponse(BaseModel):
    user_id: int
    week_start_date: str
    schedule: List[DailyMealPlan]