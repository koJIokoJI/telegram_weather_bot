from aiogram_dialog import DialogManager

from app.infrastructure.database.requests import get_default_city
from app.services.weather_service import Weather, get_weather


async def first_show_getter(dialog_manager: DialogManager, **kwargs) -> dict[str, bool]:
    start_data = dialog_manager.start_data
    if start_data:
        for key, value in start_data.items():
            dialog_manager.dialog_data[key] = value
        dialog_manager.start_data.clear()
    else:
        dialog_manager.dialog_data.update(
            show_greetings=False, show_input_city_discard_button=True
        )
    return {
        "show_greetings": dialog_manager.dialog_data.get("show_greetings"),
        "show_discard_city_input_button": dialog_manager.dialog_data.get(
            "show_discard_city_input_button"
        ),
    }


async def menu_getter(dialog_manager: DialogManager, **kwargs) -> dict[str, str | bool]:
    default_city = await get_default_city(
        session=dialog_manager.middleware_data.get("session"),
        telegram_id=kwargs.get("event_from_user").id,
    )
    cities = dialog_manager.dialog_data.get("cities")
    show_default_city_changed = dialog_manager.dialog_data.get(
        "show_default_city_changed"
    )
    quick_access_cities_restriction = dialog_manager.dialog_data.get(
        "quick_qccess_cities_restriction"
    )
    show_added_quick_access_city = dialog_manager.dialog_data.get(
        "show_added_quick_access_city"
    )
    cities = [(cities[i], i) for i in range(len(cities))] if cities else []
    getter_data = {
        "default_city": default_city,
        "cities": cities,
        "show_default_city_changed": show_default_city_changed,
        "quick_access_cities_restriction": quick_access_cities_restriction,
        "show_added_quick_access_city": show_added_quick_access_city,
    }
    return getter_data


async def weather_getter(
    dialog_manager: DialogManager, **kwargs
) -> dict[str, str | bool]:
    token = kwargs.get("token")
    current_city = dialog_manager.dialog_data.get("current_city")
    weather: Weather = await get_weather(city=current_city, token=token)
    return {
        "city": current_city,
        "time": weather.time,
        "temperature": weather.temperature_in_celsius,
        "temperature_feels_like": weather.temperature_feels_like_in_celsius,
        "pressure": weather.pressure_in_mmrtst,
        "humidity": weather.humidity,
        "wind_speed": weather.wind_speed,
    }
