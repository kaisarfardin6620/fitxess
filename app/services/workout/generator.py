from app.db.models import Exercise
from sqlalchemy.orm import Session
import random

def generate_weekly_plan(db: Session, days: int, injuries: list[str], equipment: list[str]):
    # Define splits based on available days
    if days == 3:
        split = ["Full Body", "Full Body", "Full Body"]
    elif days == 4:
        split = ["Upper", "Lower", "Rest", "Upper", "Lower"]
    else:
        split = ["Push", "Pull", "Legs", "Upper", "Lower"]

    weekly_schedule = []
    
    for day_name in split:
        if day_name == "Rest":
            continue
            
        # Logic: Fetch exercises from DB filtering by muscle group
        # This is a simplified version. In real implementation, you'd use complex SQL queries.
        daily_routine = {
            "day": "Day " + str(len(weekly_schedule) + 1),
            "focus": day_name,
            "exercises": []
        }
        
        # Mocking fetching 3 exercises per day for now
        # In reality, you query: db.query(Exercise).filter(...)
        daily_routine["exercises"].append({
            "id": 1, 
            "name": f"{day_name} Primary Move",
            "muscle_group": day_name,
            "target": {"sets": 4, "reps": "8-10"}
        })
        
        weekly_schedule.append(daily_routine)
        
    return {
        "plan_name": f"{days} Day Customized Split",
        "schedule": weekly_schedule
    }