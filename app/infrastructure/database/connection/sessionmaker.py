import asyncio

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from config.config import settings
from app.infrastructure.database.models import Base


async def get_sessionmaker():
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    engine = create_async_engine(url=settings.postgres_url, echo=False)
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)

    Sessionmaker = async_sessionmaker(engine, expire_on_commit=False)
    return Sessionmaker
