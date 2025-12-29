# app/services/nutrition/calculator.py
from app.core.nutrition_rules import MICRONUTRIENT_GUIDELINES
from app.core.constants import ACTIVITY_MULTIPLIERS, GOAL_ADJUSTMENTS

def calculate_hydration(weight_kg: float, activity_minutes: int = 0, condition: str = "none") -> int:
    """
    Formula from PDF: 
    - Body Weight (kg) * 35 ml
    - + Exercise Replacement (avg 10ml per min intensity)
    - + 300ml if Pregnant
    - + 700ml if Breastfeeding
    """
    base_water = weight_kg * 35
    
    # Exercise replacement (Using avg 10ml/min as safe middle ground between 6-14ml)
    exercise_water = activity_minutes * 10
    
    total = base_water + exercise_water
    
    if condition == "pregnant":
        total += 300
    elif condition == "breastfeeding":
        total += 700
        
    return int(total)

def get_micronutrient_targets(age: int, gender: str, condition: str = "none") -> dict:
    """
    Selects the correct row from the PDF data.
    """
    # 1. Check Special Conditions first
    if condition == "pregnant":
        return MICRONUTRIENT_GUIDELINES["pregnancy"]
    if condition == "breastfeeding":
        return MICRONUTRIENT_GUIDELINES["breastfeeding"]
        
    # 2. Check Age brackets
    if 9 <= age <= 13:
        return MICRONUTRIENT_GUIDELINES["child_9_13"]
        
    # 3. Check Gender/Age Combinations
    if gender.lower() == "male":
        if 14 <= age <= 18:
            return MICRONUTRIENT_GUIDELINES["male_14_18"]
        elif age >= 51:
            return MICRONUTRIENT_GUIDELINES["male_51_plus"]
        else: # 19-50
            return MICRONUTRIENT_GUIDELINES["male_19_50"]
            
    else: # Female
        if 14 <= age <= 18:
            return MICRONUTRIENT_GUIDELINES["female_14_18"]
        elif age >= 51:
            # Note: Vitamin D logic for 71+ can be added here if needed
            return MICRONUTRIENT_GUIDELINES["female_51_plus"]
        else: # 19-50
            return MICRONUTRIENT_GUIDELINES["female_19_50"]
            
    # Default fallback (Adult Male logic) if age < 9 or unknown
    return MICRONUTRIENT_GUIDELINES["male_19_50"]


def calculate_macros(weight: float, height: float, age: int, gender: str, goal: str, activity: str) -> dict:
    # --- EXISTING BMR/MACRO LOGIC (Keep what I gave you before) ---
    if gender.lower() == "male":
        bmr = (10 * weight) + (6.25 * height) - (5 * age) + 5
    else:
        bmr = (10 * weight) + (6.25 * height) - (5 * age) - 161

    tdee = bmr * ACTIVITY_MULTIPLIERS.get(activity.lower(), 1.2)
    target_cals = tdee + GOAL_ADJUSTMENTS.get(goal.lower(), 0)
    
    # Ratios
    if "lose" in goal.lower():
        p, f, c = 0.40, 0.25, 0.35
    elif "build" in goal.lower():
        p, f, c = 0.30, 0.25, 0.45
    else:
        p, f, c = 0.30, 0.30, 0.40

    return {
        "calories": int(target_cals),
        "protein": int((target_cals * p) / 4),
        "fats": int((target_cals * f) / 9),
        "carbs": int((target_cals * c) / 4)
    }