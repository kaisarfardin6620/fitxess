import json
from openai import OpenAI
from app.core.config import settings

client = OpenAI(api_key=settings.OPENAI_API_KEY)

def generate_monthly_meals(cals: int, protein: int, allergies: list, food_prefs: list) -> list:
    if not settings.OPENAI_API_KEY:
        return []

    prompt = f"""
    Generate a 3-day sample meal plan to repeat for a month.
    Targets: {cals} kcal, {protein}g Protein.
    Restrictions: {allergies}, Preferences: {food_prefs}.
    
    Return ONLY JSON matching this Mongoose schema structure for 'dailyMeals':
    [
      {{
        "date": "2025-01-01T00:00:00.000Z",
        "mealType": "breakfast",
        "foods": [ {{ "name": "Oats", "calories": 300, "protein": 10, "carbs": 50, "fat": 5 }} ],
        "notes": "High fiber"
      }},
      {{ "mealType": "lunch", ... }},
      {{ "mealType": "dinner", ... }},
      {{ "mealType": "snacks", ... }}
    ]
    Repeat this structure for 3 full days (Breakfast/Lunch/Dinner/Snacks for each day).
    """

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"}
    )
    
    try:
        content = json.loads(response.choices[0].message.content)
        return content.get("dailyMeals", [])
    except:
        return []