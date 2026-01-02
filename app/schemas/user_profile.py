from pydantic import BaseModel
from typing import List, Optional

class UserProfileInput(BaseModel):
    gender: str
    age: int
    height: float
    weight: float
    goal: str
    activity_level: str
    injuries: List[str] = []
    equipment: List[str] = []
    allergies: List[str] = []
    symptoms: List[str] = []
    workout_days: int = 3