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
    exerciseWantAdd: Optional[str] = None
    consistentlyWorkoutPeriod: Optional[str] = None
    workoutPlanGoal: str
    bodyPartOfImprovement: Optional[str] = None
    currentWorkoutPlace: Optional[str] = None
    isAbleToGoGym: str
    barriersToGymAccess: List[str] = []
    availableEquipment: List[str] = []
    weeklyTrainingDays: str
    workoutSession: Optional[str] = None