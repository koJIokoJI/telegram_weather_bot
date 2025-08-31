from typing import Callable, Awaitable, Any
from aiogram import BaseMiddleware
from aiogram.types import Update
from sqlalchemy.ext.asyncio import async_sessionmaker


class DbSessionMiddleware(BaseMiddleware):
    def __init__(self, session: async_sessionmaker):
        self.session = session

    async def __call__(
        self,
        handler: Callable[[Update, dict[str, Any]], Awaitable[Any]],
        event: Update,
        data: dict[str, Any],
    ):
        # 1 сессия
        async with self.session() as session:
            data["session"] = session
            return await handler(event, data)
