import asyncio
import logging
import os
import sys

from config.config import settings
from app.bot import bot
from logs.telegram_log_handler import TgHandler

logger = logging.getLogger(__name__)
tg_handler = TgHandler(bot_token=settings.log_bot_token, chat_id=settings.admin_ids[0])
tg_handler.setLevel(logging.ERROR)
logging.basicConfig(
    level=settings.logs.level,
    format=settings.logs.format,
    handlers=[tg_handler, logging.StreamHandler()],
)

if sys.platform.startswith("win") or os.name == "nt":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

asyncio.run(bot())
