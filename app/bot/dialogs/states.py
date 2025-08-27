from aiogram.fsm.state import StatesGroup, State


class WeatherSG(StatesGroup):
    city_input = State()
    quick_access_city_input = State()
    menu = State()
    weather = State()
    remove_city = State()
