from openai import OpenAI
from app.core.config import settings
import json

client = OpenAI(api_key=settings.OPENAI_API_KEY)

def parse_voice_log(text_transcript: str) -> dict:
    if not settings.OPENAI_API_KEY:
        return {"items": [{"name": "Mock Item", "calories": 0}]}

    prompt = f"""
    Extract food items and estimate nutrition from this text: "{text_transcript}".
    Return raw JSON (no markdown) with a list of 'items'. 
    Each item must have: name, quantity, calories, protein, carbs, fats.
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )
        content = response.choices[0].message.content
        content = content.replace("```json", "").replace("```", "").strip()
        return json.loads(content)
    except Exception as e:
        print(f"NLP Error: {e}")
        return {"error": "Failed to parse voice log"}