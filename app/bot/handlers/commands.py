from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode

from app.bot.dialogs import WeatherSG

commands_router = Router()


@commands_router.message(CommandStart())
async def process_start_command(message: Message, dialog_manager: DialogManager):
    await dialog_manager.start(
        state=WeatherSG.city_input,
        mode=StartMode.RESET_STACK,
        data={
            "show_greetings": True,
            "show_input_city_discard_button": False,
            "cities": [],
        },
    )
