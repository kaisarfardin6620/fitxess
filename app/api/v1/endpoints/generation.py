# app/api/v1/endpoints/generation.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

# Database & Security
from app.db.session import get_db
from app.core.security import verify_token
from app.db.models import User, Plan

# Schemas
from app.schemas.user_profile import UserProfileInput
from app.schemas.dashboard_output import DashboardResponse

# Business Logic (Services)
from app.services.nutrition import calculator, symptom_analysis

router = APIRouter()

@router.post("/generate-plan", response_model=DashboardResponse)
def generate_plan(
    user_in: UserProfileInput,
    db: Session = Depends(get_db),
    token: dict = Depends(verify_token)
):
    """
    Main AI Endpoint:
    1. Validates User via Node.js JWT.
    2. Calculates Macros (BMR/TDEE).
    3. Calculates Hydration (from PDF formula).
    4. Selects Micronutrient Targets (from PDF logic).
    5. Analyzes Symptoms (Energy/Digestion scores).
    6. Saves everything to the 'plans' table.
    """
    
    # 1. Get User ID from Token
    user_id = token.get("id")
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid User ID in token")

    # 2. Calculate Core Macros (Calories, Protein, Carbs, Fats)
    macros = calculator.calculate_macros(
        weight=user_in.weight, 
        height=user_in.height, 
        age=user_in.age, 
        gender=user_in.gender, 
        goal=user_in.goal, 
        activity=user_in.activity_level
    )
    
    # 3. Calculate Hydration (Logic from Page 6 of PDF)
    # Note: If you add 'pregnancy' status to user input later, pass it here.
    # We estimate 'activity_minutes' roughly based on workout_days * 45 mins / 7 days
    avg_daily_activity_mins = (user_in.workout_days * 45) // 7
    hydration_target = calculator.calculate_hydration(
        weight_kg=user_in.weight,
        activity_minutes=avg_daily_activity_mins,
        condition="none" # Update this if you add pregnancy status to UserProfileInput
    )
    
    # Add hydration to the macros dict to match the Response Schema
    macros["hydration_ml"] = hydration_target

    # 4. Get Micronutrient Targets (Logic from PDF Pages 1-6)
    micro_targets = calculator.get_micronutrient_targets(
        age=user_in.age, 
        gender=user_in.gender, 
        condition="none"
    )

    # 5. Analyze Symptoms (Functional Health Scores)
    # Checks for 'low_energy', 'bloating' etc. in the user's symptom list
    functional_scores = symptom_analysis.analyze_symptoms(user_in.symptoms)
    
    # 6. Generate Simple Food Recommendations (Based on deficiencies)
    # This is a basic logic placeholder. In the future, this can query your 'nutrients.csv'
    recommended_foods = []
    if "low_energy" in user_in.symptoms:
        recommended_foods.append({"name": "Spinach", "reason": "Rich in Iron for Energy"})
    if "bloating" in user_in.symptoms:
        recommended_foods.append({"name": "Ginger Tea", "reason": "Aids Digestion"})

    # 7. Save to Database (Write-Only 'plans' table)
    # We serialize the dictionaries to JSON for storage
    new_plan = Plan(
        user_id=int(user_id),
        analysis_data=functional_scores,     # Stores the [Energy: 69, Digestion: 80]
        nutrition_plan={
            "macros": macros,
            "micros": micro_targets,
            "hydration": hydration_target
        },
        workout_plan={} # Populated by a separate call or added here if needed
    )
    
    db.add(new_plan)
    db.commit()
    db.refresh(new_plan)
    
    # 8. Return JSON Response to App
    return {
        "user_id": int(user_id),
        "daily_targets": macros,          # Includes Protein, Carbs, Fats, Cals, Hydration
        "micronutrient_targets": micro_targets, # The "Minimum Targets" from PDF
        "functional_scores": functional_scores, # The "69% Energy" scores
        "recommended_foods": recommended_foods
    }