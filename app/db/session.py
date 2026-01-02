from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings

client = AsyncIOMotorClient(settings.DATABASE_URL)
database = client.get_default_database()

def get_database():
    return database