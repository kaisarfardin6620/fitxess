from pydantic import BaseModel
from typing import List, Optional

class ExerciseSet(BaseModel):
    sets: int
    reps: str # "8-12"
    weight_suggestion: Optional[str] = None # "Start with 10kg"

class ExerciseDetail(BaseModel):
    id: int
    name: str
    muscle_group: str
    video_url: Optional[str] = None
    target: ExerciseSet

class DailyWorkout(BaseModel):
    day: str # "Monday"
    focus: str # "Push", "Legs"
    exercises: List[ExerciseDetail]

class WeeklyPlanResponse(BaseModel):
    plan_name: str # "3 Day Split - Fat Loss"
    schedule: List[DailyWorkout]