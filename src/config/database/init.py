import asyncio
from config.database.db_connect import Base, engine
import domain.models

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

asyncio.run(init_db())
