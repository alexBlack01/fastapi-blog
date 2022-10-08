from datetime import datetime
from typing import Optional, List
from uuid import UUID

from motor.motor_asyncio import AsyncIOMotorClient
from odmantic import AIOEngine, Model

from adapters.config import infrastructure_config
from shared import container


class Post(Model):
    user_id: UUID
    user_id: UUID
    title: str
    content: Optional[str]
    is_published: Optional[bool]
    photo: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    likes: Optional[List[int]] = None


async def init_postgres():
    client = AsyncIOMotorClient(infrastructure_config.postgres_dsn)
    container.register(AsyncIOMotorClient, instance=client)

    engine = AIOEngine(motor_client=client, database=infrastructure_config.postgres_db_name)
    container.register(AIOEngine, instance=engine)


async def stop_postgres():
    client = container.resolve(AsyncIOMotorClient)
    await client.close()
