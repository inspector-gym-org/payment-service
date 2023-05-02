from motor.motor_asyncio import AsyncIOMotorClient

from .config import settings

client = AsyncIOMotorClient(
    host=settings.mongo_host,
    port=settings.mongo_port,
    username=settings.mongo_user,
    password=settings.mongo_pass,
)

database = client[settings.mongo_database_name]
payments_collection = database["payments"]
