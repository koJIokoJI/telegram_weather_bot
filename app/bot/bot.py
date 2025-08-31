import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.base import DefaultKeyBuilder
from aiogram.fsm.storage.redis import RedisStorage
from aiogram_dialog import setup_dialogs
from redis.asyncio import Redis, ConnectionError
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from config.config import settings
from app.infrastructure.database.models import Base
from app.bot.handlers import commands_router
from app.bot.dialogs import weather_dialog
from app.services.scheduler import broker, scheduler
from app.bot.middlewares import DbSessionMiddleware
from app.infrastructure.database.connection import get_sessionmaker

logger = logging.getLogger(__name__)


async def main():
    redis = Redis(
        host=settings.redis_host, port=settings.redis_port, db=settings.redis_db
    )
    try:
        await redis.ping()
        logger.info("Connection to Redis established")
    except ConnectionError:
        logger.error("Failed to establish connection to Redis")
        return
    logger.debug("QWEQWEQWWQEWQE")
    engine = create_async_engine(url=settings.postgres_url, echo=False)
    async with engine.begin() as connection:
        logger.debug("Creating table")
        await connection.run_sync(Base.metadata.create_all)
    storage = RedisStorage(
        redis=redis, key_builder=DefaultKeyBuilder(with_destiny=True)
    )
    bot = Bot(
        token=settings.bot_token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dp = Dispatcher(storage=storage)

    dp.include_routers(commands_router, weather_dialog)
    setup_dialogs(dp)

    Sessionmaker = async_sessionmaker(engine, expire_on_commit=False)
    dp.update.outer_middleware(DbSessionMiddleware(session=Sessionmaker))

    await broker.startup()
    logger.info("Broker started")
    try:
        await asyncio.gather(dp.start_polling(bot, token=settings.open_weather_token))
    except (KeyboardInterrupt, asyncio.CancelledError):
        logger.info("User intervention. Exitting")
    except Exception as e:
        logger.exception(e)
    finally:
        await redis.close()
        logger.info("Connection to Redis closed")
        await broker.shutdown()
        logger.info("Connection to taskiq-broker closed")
        await bot.session.close()
        logger.info("Bot session closed")
