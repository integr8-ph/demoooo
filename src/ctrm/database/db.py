from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from src.ctrm.config.settings import get_settings
from src.ctrm.models import gather_models


async def init_db() -> None:
    client = AsyncIOMotorClient(get_settings().DATABASE_URL)
    await init_beanie(
        client[get_settings().COLLECTION_NAME], document_models=gather_models()
    )
