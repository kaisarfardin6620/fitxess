from fastapi import APIRouter, Depends, HTTPException
from app.db.session import get_database
from app.core.security import verify_token
from app.services.nutrition import calculator, meal_generator
from app.services.workout import generator as workout_generator
from bson import ObjectId
from datetime import datetime

router = APIRouter()

@router.post("/generate-all")
async def generate_all_plans(token: dict = Depends(verify_token)):
    db = get_database()
    user_id_str = token.get("id")
    if not user_id_str:
        raise HTTPException(status_code=401, detail="Invalid Token")
    
    user_oid = ObjectId(user_id_str)

    bio_info = await db.biologicalinformations.find_one({"userId": user_oid})
    onboard = await db.onboardingassessments.find_one({"userId": user_oid})
    quiz = await db.workoutonboardingquizzes.find_one({"userId": user_oid})

    if not bio_info or not onboard:
        raise HTTPException(status_code=400, detail="User onboarding incomplete")

    try:
        age = int(bio_info.get("age", 25))
        weight_kg = float(bio_info.get("weight", 70))
        height_cm = float(bio_info.get("height", 170))
    except:
        age, weight_kg, height_cm = 25, 70.0, 170.0

    gender = bio_info.get("gender", "male")
    goal_list = onboard.get("fitnessGoal", ["maintain"])
    goal = goal_list[0] if goal_list else "maintain"
    activity = onboard.get("activityLevel", "moderate")
    
    macro_result = calculator.calculate_macros(weight_kg, height_cm, age, gender, goal, activity)
    
    hydra_result = calculator.calculate_hydration(weight_kg, 30, "none")
    
    micro_result = calculator.get_micronutrient_targets(age, gender, "none")

    user_goals_data = {
        "userId": user_oid,
        "biologicalInformationId": bio_info["_id"],
        "onboardingAssesmentId": onboard["_id"],
        "date": datetime.utcnow(),
        "calories": macro_result["calories"],
        "macros": macro_result["macros"],
        "waterIntake": hydra_result,
        "categories": micro_result
    }
    
    await db.usergoals.insert_one(user_goals_data)

    allergies = onboard.get("medicalConditions", []) 
    prefs = onboard.get("foodTypes", [])
    
    generated_meals = meal_generator.generate_monthly_meals(
        cals=macro_result["calories"]["target"],
        protein=macro_result["macros"]["protein"]["target"],
        allergies=allergies,
        food_prefs=prefs
    )

    meal_plan_data = {
        "userId": user_oid,
        "biologicalInformationId": bio_info["_id"],
        "onboardingAssesmentId": onboard["_id"],
        "month": datetime.utcnow().month,
        "year": datetime.utcnow().year,
        "dailyMeals": generated_meals
    }
    
    await db.usermonthlymealplans.insert_one(meal_plan_data)

    workout_days_str = quiz.get("weeklyTraningDays", "3")
    try:
        w_days = int(workout_days_str.split()[0]) 
    except:
        w_days = 3

    injuries = quiz.get("barriersToGymAccess", []) 
    equip = quiz.get("availableEquipment", [])
    w_goal = quiz.get("workoutPlanGoal", "strength")
    
    generated_workouts = workout_generator.generate_weekly_workout(
        days_count=w_days,
        injuries=injuries,
        equipment=equip,
        goal=w_goal,
        level=quiz.get("currentActiveness", "beginner")
    )

    workout_plan_data = {
        "userId": user_oid,
        "onboardingAssesmentId": onboard["_id"],
        "title": f"AI Plan for {w_goal}",
        "weekStartDate": datetime.utcnow(),
        "days": generated_workouts
    }

    await db.userweeklyworkoutplans.insert_one(workout_plan_data)

    return {"status": "success", "message": "All plans generated and saved to MongoDB"}