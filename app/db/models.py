from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, JSON, DateTime, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.session import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    gender = Column(String, nullable=True) 
    age = Column(Integer, nullable=True)
    height = Column(Float, nullable=True)
    weight = Column(Float, nullable=True)
    activity_level = Column(String, nullable=True)
    goal = Column(String, nullable=True)
    injuries = Column(JSON, nullable=True)    
    equipment = Column(JSON, nullable=True)
    allergies = Column(JSON, nullable=True)
    food_preferences = Column(JSON, nullable=True) 
    plans = relationship("Plan", back_populates="owner")


class Plan(Base):
    __tablename__ = "plans"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    analysis_data = Column(JSON) 
    nutrition_plan = Column(JSON)
    workout_plan = Column(JSON)
    owner = relationship("User", back_populates="plans")


class Exercise(Base):
    __tablename__ = "exercises"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    muscle_group = Column(String, index=True)
    equipment = Column(String)
    difficulty = Column(String)
    video_url = Column(String, nullable=True)
    image_url = Column(String, nullable=True)
    instructions = Column(Text, nullable=True)
    bad_for_injuries = Column(JSON, nullable=True)