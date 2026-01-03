from fastapi import APIRouter, Depends, HTTPException
from app.db.session import get_database
from app.core.security import verify_token
from app.services.nutrition import calculator, meal_generator
from app.services.workout import generator as workout_generator
from bson import ObjectId
from datetime import datetime, timedelta

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
        "onboardingAssessmentId": onboard["_id"],
        "date": datetime.utcnow(),
        "calories": macro_result["calories"],
        "macros": macro_result["macros"],
        "waterIntake": hydra_result
    }
    
    goals_insert = await db.usergoals.insert_one(user_goals_data)
    goals_id = goals_insert.inserted_id

    category_docs = []
    for cat_name, items in micro_result.items():
        if cat_name not in ['energy', 'digestion', 'immunity']:
            continue
        for item in items:
            category_docs.append({
                "goalsId": goals_id,
                "userId": user_oid,
                "category": cat_name,
                "name": item["name"],
                "target": item["target"],
                "consumed": 0,
                "isGoodIfHigh": item.get("isGoodIfHight", True)
            })
    
    if category_docs:
        await db.categoryitems.insert_many(category_docs)

    allergies = onboard.get("medicalConditions", []) 
    prefs = onboard.get("foodTypes", [])
    
    generated_days_data = meal_generator.generate_monthly_meals(
        cals=macro_result["calories"]["target"],
        protein=macro_result["macros"]["protein"]["target"],
        allergies=allergies,
        food_prefs=prefs
    )

    monthly_plan_data = {
        "userId": user_oid,
        "biologicalInformationId": bio_info["_id"],
        "onboardingAssessmentId": onboard["_id"],
        "month": datetime.utcnow().month,
        "year": datetime.utcnow().year
    }
    
    monthly_insert = await db.usermonthlymealplans.insert_one(monthly_plan_data)
    monthly_id = monthly_insert.inserted_id

    for day_data in generated_days_data:
        day_offset = day_data.get("dayOffset", 0)
        current_date = datetime.utcnow() + timedelta(days=day_offset)
        
        meals_list = day_data.get("meals", [])
        if not isinstance(meals_list, list): 
            continue

        for meal in meals_list:
            daily_doc = {
                "mealPlanId": monthly_id,
                "userId": user_oid,
                "date": current_date,
                "mealType": meal.get("mealType", "snacks"),
                "notes": meal.get("notes", "")
            }
            daily_insert = await db.userdailymealplans.insert_one(daily_doc)
            daily_id = daily_insert.inserted_id
            
            foods = meal.get("foods", [])
            food_docs = []
            for f in foods:
                food_docs.append({
                    "mealPlanId": monthly_id,
                    "mealDayId": daily_id,
                    "userId": user_oid,
                    "name": f.get("name"),
                    "calories": f.get("calories"),
                    "protein": f.get("protein"),
                    "carbs": f.get("carbs"),
                    "fat": f.get("fat")
                })
            
            if food_docs:
                await db.fooditems.insert_many(food_docs)

    workout_days_str = quiz.get("weeklyTrainingDays", "3")
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
        "onboardingAssessmentId": onboard["_id"],
        "title": f"AI Plan for {w_goal}",
        "weekStartDate": datetime.utcnow(),
        "weekEndDate": datetime.utcnow() + timedelta(days=7)
    }

    weekly_insert = await db.userweeklyworkoutplans.insert_one(workout_plan_data)
    weekly_id = weekly_insert.inserted_id

    if isinstance(generated_workouts, list):
        for w_session in generated_workouts:
            session_doc = {
                "workoutPlanId": weekly_id,
                "userId": user_oid,
                "title": w_session.get("title", "Workout"),
                "workoutType": w_session.get("workoutType", "strength"),
                "intensity": w_session.get("intensity", "medium"),
                "estimatedCaloriesBurn": w_session.get("estimatedCaloriesBurn", 300),
                "isCompleted": False
            }
            
            session_insert = await db.dailyworkoutsessions.insert_one(session_doc)
            session_id = session_insert.inserted_id
            
            exercises = w_session.get("exercises", [])
            ex_docs = []
            for ex in exercises:
                ex_docs.append({
                    "workoutSessionId": session_id,
                    "workoutPlanId": weekly_id,
                    "userId": user_oid,
                    "name": ex.get("name"),
                    "muscleGroups": ex.get("muscleGroups", []),
                    "durationMin": ex.get("durationMin"),
                    "sets": ex.get("sets"),
                    "reps": ex.get("reps"),
                    "restSeconds": ex.get("restSeconds"),
                    "weight": ex.get("weight"),
                    "isCompleted": False
                })
            
            if ex_docs:
                await db.exercises.insert_many(ex_docs)

    return {"status": "success", "message": "All plans generated and normalized to MongoDB"}