import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.base import DefaultKeyBuilder
from aiogram.fsm.storage.redis import RedisStorage
from aiogram_dialog import setup_dialogs
from redis.asyncio import Redis

from config.config import settings
from app.bot.handlers import commands_router
from app.bot.dialogs import weather_dialog
from app.services.scheduler import broker, scheduler

logger = logging.getLogger(__name__)


async def main():
    redis = Redis(
        host=settings.redis_host, port=settings.redis_port, db=settings.redis_db
    )
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
        logger.info("Connection t Redis closed")
        await broker.shutdown()
        logger.info("Connection to taskiq-broker closed")
        await bot.session.close()
        logger.info("Bot session closed")
