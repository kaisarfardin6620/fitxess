from app.core.nutrition_rules import MICRONUTRIENT_GUIDELINES, STANDARD_LIMITS

ACTIVITY_MULTIPLIERS = {
    "sedentary": 1.2,
    "light": 1.375,
    "moderate": 1.55,
    "active": 1.725,
    "very_active": 1.9
}

GOAL_ADJUSTMENTS = {
    "lose_weight": -500,
    "maintain": 0,
    "gain_muscle": 300
}

def calculate_hydration(weight_kg: float, activity_minutes: int = 0, condition: str = "none") -> dict:
    base_water = weight_kg * 35
    exercise_water = activity_minutes * 10
    total_ml = base_water + exercise_water
    
    if condition.lower() == "pregnant":
        total_ml += 300
    elif condition.lower() == "breastfeeding":
        total_ml += 700
        
    return {
        "targetOz": int(total_ml * 0.033814),
        "consumedOz": 0
    }

def get_micronutrient_targets(age: int, gender: str, condition: str = "none") -> dict:
    targets = {}
    
    if condition.lower() == "pregnant":
        targets = MICRONUTRIENT_GUIDELINES["pregnancy"]
    elif condition.lower() == "breastfeeding":
        targets = MICRONUTRIENT_GUIDELINES["breastfeeding"]
    elif 9 <= age <= 13:
        targets = MICRONUTRIENT_GUIDELINES["child_9_13"]
    else:
        if gender.lower() == "male":
            if 14 <= age <= 18:
                targets = MICRONUTRIENT_GUIDELINES["male_14_18"]
            elif age >= 51:
                targets = MICRONUTRIENT_GUIDELINES["male_51_plus"]
            else:
                targets = MICRONUTRIENT_GUIDELINES["male_19_50"]
        else:
            if 14 <= age <= 18:
                targets = MICRONUTRIENT_GUIDELINES["female_14_18"]
            elif age >= 51:
                targets = MICRONUTRIENT_GUIDELINES["female_51_plus"]
            else:
                targets = MICRONUTRIENT_GUIDELINES["female_19_50"]
    
    final_categories = {
        "energy": [],
        "digestion": [],
        "immunity": []
    }

    for name, val in targets.items():
        item = {"name": name, "target": val, "consumed": 0, "isGoodIfHight": True}
        if name in ["B1", "B2", "B3", "B5", "B6", "B12", "Iron", "Magnesium"]:
            final_categories["energy"].append(item)
        if name in ["Vitamin D", "Zinc"]:
            final_categories["immunity"].append(item)

    final_categories["digestion"].append({"name": "Fiber", "target": STANDARD_LIMITS["fiber"], "consumed": 0, "isGoodIfHight": True})
    final_categories["energy"].append({"name": "Sugar", "target": STANDARD_LIMITS["sugar"], "consumed": 0, "isGoodIfHight": False})
    final_categories["immunity"].append({"name": "Sodium", "target": STANDARD_LIMITS["sodium"], "consumed": 0, "isGoodIfHight": False})
    
    return final_categories

def calculate_macros(weight: float, height: float, age: int, gender: str, goal: str, activity: str) -> dict:
    if gender.lower() == "male":
        bmr = (10 * weight) + (6.25 * height) - (5 * age) + 5
    else:
        bmr = (10 * weight) + (6.25 * height) - (5 * age) - 161

    tdee = bmr * ACTIVITY_MULTIPLIERS.get(activity.lower(), 1.2)
    
    target_cals = tdee
    if "lean" in goal.lower() or "fat" in goal.lower():
        target_cals -= 500
        p, f, c = 0.40, 0.25, 0.35
    elif "build" in goal.lower() or "muscle" in goal.lower():
        target_cals += 300
        p, f, c = 0.30, 0.25, 0.45
    else:
        p, f, c = 0.30, 0.30, 0.40

    cals = int(target_cals)
    
    return {
        "calories": {"target": cals, "consumed": 0},
        "macros": {
            "protein": {"target": int((cals * p) / 4), "consumed": 0},
            "fat": {"target": int((cals * f) / 9), "consumed": 0},
            "carbs": {"target": int((cals * c) / 4), "consumed": 0}
        }
    }