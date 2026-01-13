import json
from openai import OpenAI
from app.core.config import settings

client = OpenAI(api_key=settings.OPENAI_API_KEY)

def generate_weekly_workout(days_count: int, injuries: list, equipment: list, goal: str, level: str) -> list:
    if not settings.OPENAI_API_KEY:
        return []

    prompt = f"""
    Create a weekly workout plan.
    Days per week: {days_count}. Goal: {goal}. Level: {level}.
    Equipment: {equipment}. Injuries to avoid: {injuries}.
    
    Return a JSON OBJECT with a key "days" containing a list.
    Structure:
    {{
      "days": [
        {{
            "title": "Leg Day",
            "workoutType": "strength",
            "intensity": "high",
            "estimatedCaloriesBurn": 400,
            "exercises": [
              {{
                "name": "Squats",
                "muscleGroups": ["legs"],
                "durationMin": 10,
                "sets": 3,
                "reps": 12,
                "restSeconds": 60,
                "weight": 20
              }}
            ]
        }}
      ]
    }}
    Generate exactly {days_count} days.
    """

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )


        content = json.loads(response.choices[0].message.content)
        return content.get("days", [])
        
    except Exception as e:
        print(f"DEBUG WORKOUT ERROR: {e}")
        return []