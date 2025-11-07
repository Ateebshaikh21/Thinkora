import os
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import ConnectionFailure
import logging
from dotenv import load_dotenv

load_dotenv()

class Database:
    client: AsyncIOMotorClient = None
    database = None

db = Database()

async def connect_to_mongo():
    """Create database connection"""
    try:
        mongodb_url = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
        db_name = os.getenv("DATABASE_NAME", "thinkora")
        
        db.client = AsyncIOMotorClient(mongodb_url, serverSelectionTimeoutMS=5000)
        db.database = db.client[db_name]
        
        # Test the connection with shorter timeout
        await db.client.admin.command('ping')
        logging.info(f"Connected to MongoDB at {mongodb_url}")
        
    except Exception as e:
        logging.error(f"Failed to connect to MongoDB: {e}")
        # Don't raise the error, just log it for development
        db.client = None
        db.database = None

async def close_mongo_connection():
    """Close database connection"""
    if db.client:
        db.client.close()
        logging.info("Disconnected from MongoDB")

def get_database():
    """Get database instance"""
    return db.database

# Collections
def get_subjects_collection():
    if db.database is None:
        return None
    return db.database.subjects

def get_sessions_collection():
    if db.database is None:
        return None
    return db.database.study_sessions

def get_questions_collection():
    if db.database is None:
        return None
    return db.database.questions