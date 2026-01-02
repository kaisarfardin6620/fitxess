from pydantic import BaseModel
from typing import List, Optional

class ExerciseSet(BaseModel):
    sets: int
    reps: str
    weight_suggestion: Optional[str] = None

class ExerciseDetail(BaseModel):
    id: int
    name: str
    muscle_group: str
    video_url: Optional[str] = None
    target: ExerciseSet

class DailyWorkout(BaseModel):
    day: str
    focus: str
    exercises: List[ExerciseDetail]

class WeeklyPlanResponse(BaseModel):
    plan_name: str
    schedule: List[DailyWorkout]