from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from models import Book

async def init_db():
    client = AsyncIOMotorClient("mongodb://localhost:27017")
    db = client["book_db"]
    await init_beanie(database=db, document_models=[Book])
