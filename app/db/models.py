# app/db/models.py
from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, JSON, DateTime, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.session import Base

# --- 1. USER PROFILE (Read-Only) ---
# Mirrors the table created by your Node.js backend.
# Ensure the table name "users" matches exactly what is in your DB.
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    
    # Biometrics & Profile
    # Using nullable=True because a new user might not have finished onboarding
    gender = Column(String, nullable=True) 
    age = Column(Integer, nullable=True)
    height = Column(Float, nullable=True)  # stored in cm
    weight = Column(Float, nullable=True)  # stored in kg
    activity_level = Column(String, nullable=True) # e.g., "sedentary"
    goal = Column(String, nullable=True) # e.g., "muscle_gain"
    
    # Complex Data (Stored as JSON Arrays)
    # Node.js will save: ["knee_pain", "lower_back"]
    injuries = Column(JSON, nullable=True)    
    equipment = Column(JSON, nullable=True)   # ["dumbbell", "barbell"]
    allergies = Column(JSON, nullable=True)   # ["peanuts", "dairy"]
    food_preferences = Column(JSON, nullable=True) 
    
    # Relationship to generated plans
    plans = relationship("Plan", back_populates="owner")


# --- 2. GENERATED PLANS (Write-Only) ---
# This is where the AI saves the result.
class Plan(Base):
    __tablename__ = "plans"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # The Analysis Results (Energy score, Digestion score)
    analysis_data = Column(JSON) 
    
    # The Actual Plans
    nutrition_plan = Column(JSON) # { "calories": 2500, "meals": {...} }
    workout_plan = Column(JSON)   # { "monday": ["bench_press"], ... }
    
    owner = relationship("User", back_populates="plans")


# --- 3. EXERCISE DATABASE (Static Data) ---
# This table will be populated by your CSV Script later.
class Exercise(Base):
    __tablename__ = "exercises"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    muscle_group = Column(String, index=True) # Chest, Back, Legs
    equipment = Column(String)    # Dumbbell, Machine, Bodyweight
    difficulty = Column(String)   # Beginner, Intermediate
    
    # Media & Instructions
    video_url = Column(String, nullable=True)
    image_url = Column(String, nullable=True)
    instructions = Column(Text, nullable=True)
    
    # Logic for AI filtering
    bad_for_injuries = Column(JSON, nullable=True) # ["shoulder", "wrist"]