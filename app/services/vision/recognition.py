# app/services/vision/recognition.py
import base64
import json
from openai import OpenAI
from app.core.config import settings

client = OpenAI(api_key=settings.OPENAI_API_KEY)

def analyze_food_image(image_bytes: bytes) -> dict:
    if not settings.OPENAI_API_KEY:
        # Mock response if no key provided
        return {"name": "Test Food", "calories": 100, "protein": 5, "carbs": 10, "fats": 2}

    base64_image = base64.b64encode(image_bytes).decode('utf-8')

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "Identify the food in this image. Return a raw JSON object (no markdown) with keys: name, calories, protein, carbs, fats."},
                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}},
                    ],
                }
            ],
            max_tokens=300,
        )
        content = response.choices[0].message.content
        # Clean potential markdown wrappers
        content = content.replace("```json", "").replace("```", "").strip()
        return json.loads(content)
    except Exception as e:
        print(f"Error calling OpenAI: {e}")
        return {"error": "Failed to analyze image"}