# app/db/base.py
from app.db.session import Base
from app.db.models import User, Plan, Exercise
# Import all other models here so Alembic can "see" them