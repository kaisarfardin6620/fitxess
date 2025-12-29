# app/services/nutrition/meal_generator.py
from typing import List
from app.schemas.meal_plan import DailyMealPlan, MealItem

def generate_weekly_meals(target_macros: dict, preferences: List[str] = []) -> List[DailyMealPlan]:
    """
    Generates a mock 7-day plan based on target calories.
    In production, this queries your FoodDB.
    """
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    schedule = []

    # Simple logic to split calories roughly
    cals = target_macros.get("calories", 2000)
    bf_cals = int(cals * 0.25)
    ln_cals = int(cals * 0.35)
    dn_cals = int(cals * 0.30)
    sn_cals = int(cals * 0.10)

    for day in days:
        daily_plan = DailyMealPlan(
            day=day,
            total_calories=cals,
            meals={
                "breakfast": MealItem(name="Oatmeal & Berries", calories=bf_cals, protein=15, carbs=40, fats=5),
                "lunch": MealItem(name="Grilled Chicken Salad", calories=ln_cals, protein=40, carbs=10, fats=15),
                "dinner": MealItem(name="Salmon & Quinoa", calories=dn_cals, protein=35, carbs=30, fats=20),
                "snack": MealItem(name="Greek Yogurt", calories=sn_cals, protein=12, carbs=8, fats=0),
            }
        )
        schedule.append(daily_plan)
        
    return schedule