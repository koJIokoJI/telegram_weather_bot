from aiogram.types import Message, CallbackQuery
from aiogram_dialog import DialogManager, ShowMode
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.input import MessageInput, ManagedTextInput

from app.bot.dialogs import WeatherSG
from app.infrastructure.database import insert_user


def city_check(city: str) -> str | ValueError:
    if all(char.isalpha() or char == "-" for char in city) and 3 <= len(city) <= 180:
        return city
    raise ValueError


async def incorrect_message_type(
    message: Message, widget: MessageInput, dialog_manager: DialogManager
) -> None:
    dialog_manager.show_mode = ShowMode.NO_UPDATE
    await message.answer(text="Введите название города <b>текстом</b>")


async def correct_city_check_handler(
    message: Message,
    widget: ManagedTextInput,
    dialog_manager: DialogManager,
    city: str,
) -> None:
    city = city.lower().capitalize()
    session = dialog_manager.middleware_data.get("session")
    if "-" in city:
        hyphen = city.find("-")
        city = city[:hyphen].capitalize() + "-" + city[hyphen + 1 :].capitalize()
    if dialog_manager.dialog_data.get("quick_access_city"):
        dialog_manager.dialog_data["cities"].append(city)
        await insert_user(
            session=session,
            telegram_id=message.from_user.id,
            default_city=dialog_manager.dialog_data["default_city"],
            cities=dialog_manager.dialog_data["cities"],
        )
    else:
        await insert_user(
            session=session,
            telegram_id=message.from_user.id,
            default_city=city,
            cities=dialog_manager.dialog_data["cities"],
        )
        dialog_manager.dialog_data.update(
            default_city=city, show_default_city_changed=True
        )
    await dialog_manager.switch_to(
        state=WeatherSG.menu, show_mode=ShowMode.DELETE_AND_SEND
    )


async def incorrect_city_check_handler(
    message: Message,
    widget: ManagedTextInput,
    dialog_manager: DialogManager,
    error: ValueError,
) -> None:
    dialog_manager.show_mode = ShowMode.NO_UPDATE
    await message.answer(
        text="Введено <b>некорректное</b> название города. <b>Попробуйте еще раз</b>"
    )


async def print_weather_handler(
    callback: CallbackQuery,
    button: Button,
    dialog_manager: DialogManager,
    *args,
) -> None:
    if button.widget_id == "default_city":
        current_city = dialog_manager.dialog_data.get("default_city")
    else:
        current_city = dialog_manager.dialog_data.get("cities")[int(args[0])]
    dialog_manager.dialog_data.update(
        current_city=current_city,
        show_default_city_changed=False,
        quick_access_cities_restriction=False,
        show_added_quick_access_city=False,
    )
    await dialog_manager.switch_to(state=WeatherSG.weather)


async def change_default_city_handler(
    callback: CallbackQuery, button: Button, dialog_manager: DialogManager
):
    dialog_manager.dialog_data.update(
        show_default_city_changed=True,
        quick_access_cities_restriction=False,
        show_added_quick_access_city=False,
        quick_access_city=False,
    )
    await dialog_manager.switch_to(state=WeatherSG.city_input)


async def add_quick_access_city_handler(
    callback: CallbackQuery, button: Button, dialog_manager: DialogManager
):
    cities = dialog_manager.dialog_data.get("cities")
    if cities != []:
        if len(cities) == 3:
            dialog_manager.dialog_data.update(
                quick_access_cities_restriction=True,
                show_added_quick_access_city=False,
            )
            await dialog_manager.switch_to(state=WeatherSG.menu)
        else:
            dialog_manager.dialog_data.update(quick_access_city=True)
            await dialog_manager.switch_to(state=WeatherSG.city_input)
    else:
        dialog_manager.dialog_data.update(quick_access_city=True)
        await dialog_manager.switch_to(state=WeatherSG.city_input)


async def switch_to_remove_quick_access_city_handler(
    callback: CallbackQuery, button: Button, dialog_manager: DialogManager
):
    dialog_manager.dialog_data.update(show_added_quick_access_city=False)
    await dialog_manager.switch_to(state=WeatherSG.remove_city)


async def remove_quick_access_city_handler(
    callback: CallbackQuery, button: Button, dialog_manager: DialogManager
):
    checked = dialog_manager.find("cities_to_remove").get_checked()
    cities = dialog_manager.dialog_data.get("cities")
    cities_to_remove = [cities[int(i)] for i in checked]
    cities = list(set(cities) - set(cities_to_remove))
    dialog_manager.current_context().widget_data["cities_to_remove"] = []
    dialog_manager.dialog_data.update(
        cities=cities,
        quick_access_cities_restriction=False,
        show_default_city_changed=False,
    )
    await dialog_manager.switch_to(state=WeatherSG.menu)


async def discard_changes_button_handler(
    callback: CallbackQuery, button: Button, dialog_manager: DialogManager
):
    dialog_manager.dialog_data.update(show_default_city_changed=False)
    await dialog_manager.switch_to(state=WeatherSG.menu)
