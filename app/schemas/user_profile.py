from pydantic import BaseModel
from typing import List, Optional

class UserProfileInput(BaseModel):
    # Core
    gender: str
    age: int
    height: float # cm
    weight: float # kg
    goal: str     # "lose_fat", "build_muscle", "maintain"
    activity_level: str # "sedentary", "moderate", "active"
    
    # Detailed Context
    injuries: List[str] = []     # ["knee", "lower_back"]
    equipment: List[str] = []    # ["dumbbell", "barbell"]
    allergies: List[str] = []
    symptoms: List[str] = []     # ["low_energy", "brain_fog"]
    workout_days: int = 3        # Days per week available