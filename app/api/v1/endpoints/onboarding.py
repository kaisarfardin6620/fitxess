from fastapi import APIRouter, Depends
from app.db.session import get_database
from app.core.security import verify_token
from app.schemas.onboarding_input import BiologicalInfoSchema, AssessmentSchema, WorkoutQuizSchema
from bson import ObjectId
from datetime import datetime

router = APIRouter()

@router.post("/biological-info")
async def save_biological_info(data: BiologicalInfoSchema, token: dict = Depends(verify_token)):
    db = get_database()
    user_id = token.get("id")
    
    doc = data.model_dump()
    doc["userId"] = ObjectId(user_id)
    doc["updatedAt"] = datetime.utcnow()
    doc["createdAt"] = datetime.utcnow()

    await db.biologicalinformations.update_one(
        {"userId": ObjectId(user_id)},
        {"$set": doc},
        upsert=True
    )
    return {"status": "saved", "step": "biological-info"}

@router.post("/assessment")
async def save_assessment(data: AssessmentSchema, token: dict = Depends(verify_token)):
    db = get_database()
    user_id = token.get("id")
    
    doc = data.model_dump()
    doc["userId"] = ObjectId(user_id)
    doc["updatedAt"] = datetime.utcnow()

    await db.onboardingassessments.update_one(
        {"userId": ObjectId(user_id)},
        {"$set": doc},
        upsert=True
    )
    return {"status": "saved", "step": "assessment"}

@router.post("/workout-quiz")
async def save_workout_quiz(data: WorkoutQuizSchema, token: dict = Depends(verify_token)):
    db = get_database()
    user_id = token.get("id")
    
    doc = data.model_dump()
    doc["userId"] = ObjectId(user_id)
    doc["updatedAt"] = datetime.utcnow()

    await db.workoutonboardingquizzes.update_one(
        {"userId": ObjectId(user_id)},
        {"$set": doc},
        upsert=True
    )
    return {"status": "saved", "step": "workout-quiz"}