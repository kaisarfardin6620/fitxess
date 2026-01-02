from pydantic import BaseModel
from typing import List, Optional

class BiologicalInfoSchema(BaseModel):
    gender: str
    age: str
    height: str
    weight: str
    bodyFat: Optional[str] = None
    muscleMass: Optional[str] = None
    state: Optional[str] = None

class AssessmentSchema(BaseModel):
    fitnessGoal: List[str]
    activityLevel: str
    exerciseLevel: Optional[str] = None
    workoutsType: List[str] = []
    eatingHabits: List[str] = []
    dailyMeals: int
    foodTypes: List[str] = []
    unusualSynonyms: List[str] = []
    medicalConditions: List[str] = []

class WorkoutQuizSchema(BaseModel):
    currentActiveness: str
    exeriseWantAdd: Optional[str] = None
    consistentlyWorkoutPriod: Optional[str] = None
    workoutPlanGoal: str
    bordyPartOfImprovement: Optional[str] = None
    currentWorkoutPlase: Optional[str] = None
    isAbleToGoGym: str
    barriersToGymAccess: List[str] = []
    availableEquipment: List[str] = []
    weeklyTraningDays: str
    workoutSession: Optional[str] = None