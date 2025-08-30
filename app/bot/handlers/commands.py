from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode
from sqlalchemy.ext.asyncio import AsyncSession

from app.bot.dialogs import WeatherSG
from app.infrastructure.database import get_user, insert_user

commands_router = Router()


@commands_router.message(CommandStart())
async def process_start_command(
    message: Message, session: AsyncSession, dialog_manager: DialogManager
):
    user = await get_user(session=session, telegram_id=message.from_user.id)
    if user is None:
        await insert_user(session=session, telegram_id=message.from_user.id)
    await dialog_manager.start(
        state=WeatherSG.city_input,
        mode=StartMode.RESET_STACK,
        data={
            "show_greetings": True,
            "show_input_city_discard_button": False,
            "cities": [],
        },
    )
