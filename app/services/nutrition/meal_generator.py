import json
from openai import OpenAI
from app.core.config import settings

client = OpenAI(api_key=settings.OPENAI_API_KEY)

def generate_monthly_meals(cals: int, protein: int, allergies: list, food_prefs: list) -> list:
    if not settings.OPENAI_API_KEY:
        return []

    prompt = f"""
    Generate a 7-DAY MEAL PLAN (1 Week Cycle).
    Targets: {cals} kcal, {protein}g Protein.
    Restrictions: {allergies}, Preferences: {food_prefs}.
    
    Return ONLY JSON matching this structure:
    [
      {{
        "dayIndex": 0,
        "meals": [
          {{
            "mealType": "breakfast",
            "notes": "Quick prep",
            "foods": [ {{ "name": "Oats", "calories": 300, "protein": 10, "carbs": 50, "fat": 5 }} ]
          }},
          {{ "mealType": "lunch", "foods": [...] }},
          {{ "mealType": "dinner", "foods": [...] }},
          {{ "mealType": "snacks", "foods": [...] }}
        ]
      }}
    ]
    Generate exactly 7 days (Index 0 to 6).
    """

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"}
    )
    
    try:
        content = json.loads(response.choices[0].message.content)
        return content.get("days", content if isinstance(content, list) else [])
    except:
        return []