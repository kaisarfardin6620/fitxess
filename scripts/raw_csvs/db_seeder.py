# scripts/db_seeder.py
import json
import os
import sys

# Add the parent directory to path so we can import 'app'
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from app.db.session import SessionLocal, engine
from app.db.models import Base, Exercise

# Define paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
JSON_FILE = os.path.join(BASE_DIR, "exercises_clean.json")

def seed_exercises():
    # Create tables if they don't exist
    Base.metadata.create_all(bind=engine)
    
    db: Session = SessionLocal()
    
    if not os.path.exists(JSON_FILE):
        print("Clean JSON not found. Run etl_cleaner.py first.")
        return

    print("Loading JSON...")
    with open(JSON_FILE, "r") as f:
        data = json.load(f)
        
    print(f"Found {len(data)} exercises. Inserting...")
    
    for item in data:
        # Create Exercise Object (Adjust keys to match your JSON)
        ex = Exercise(
            name=item.get("name"),
            muscle_group=item.get("muscle_group"),
            equipment=item.get("equipment"),
            difficulty=item.get("difficulty"),
            video_url=item.get("video_url"),
            image_url=item.get("image_url"),
            instructions=item.get("instructions"),
            # Ensure bad_for_injuries is a list, typically stored as string in CSV
            # bad_for_injuries=item.get("bad_for_injuries", "").split(",") 
        )
        db.add(ex)
        
    db.commit()
    db.close()
    print("Database seeded successfully!")

if __name__ == "__main__":
    seed_exercises()