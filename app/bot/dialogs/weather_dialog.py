import logging
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.kbd import (
    Button,
    Back,
    Select,
    Multiselect,
    Column,
    Row,
)
from aiogram_dialog.widgets.input import TextInput

from app.bot.dialogs import WeatherSG
from app.bot.dialogs.handlers import (
    city_check,
    correct_city_check_handler,
    incorrect_city_check_handler,
    print_weather_handler,
    change_default_city_handler,
    add_quick_access_city_handler,
    switch_to_remove_quick_access_city_handler,
    remove_quick_access_city_handler,
    discard_changes_button_handler,
)
from app.bot.dialogs.getters import first_show_getter, menu_getter, weather_getter

logger = logging.getLogger(__name__)


weather_dialog = Dialog(
    Window(
        Const(
            text="🖐Здравствуйте! Это бот, показывающий погоду в вашем городе",
            when="show_greetings",
        ),
        Const(text="<b>Введите город</b>:"),
        TextInput(
            id="city_input",
            type_factory=city_check,
            on_success=correct_city_check_handler,
            on_error=incorrect_city_check_handler,
        ),
        getter=first_show_getter,
        state=WeatherSG.city_input,
    ),
    Window(
        Format(
            text="<b>{default_city}</b> выбран городом по умолчанию\n",
            when="show_default_city_changed",
        ),
        Const(
            text="Город добавлен в быстрый доступ\n",
            when="show_added_quick_access_city",
        ),
        Const(
            text="Быстрый доступ ограничен 3 городами\nПеред добавлением удалите город из быстрого доступа\n",
            when="quick_access_cities_restriction",
        ),
        Const(text="<b>Меню</b>"),
        Button(
            text=Format(text="Погода в {default_city}"),
            id="default_city",
            on_click=print_weather_handler,
        ),
        Column(
            Select(
                text=Format(text="Погода в {item[0]}"),
                id="city",
                item_id_getter=lambda x: x[1],
                items="cities",
                on_click=print_weather_handler,
            )
        ),
        Button(
            text=Const(text="Изменить город по умолчанию"),
            id="change_default_city_button",
            on_click=change_default_city_handler,
        ),
        Button(
            text=Const(text="Добавить город в быстрый доступ"),
            id="add_quick_access_city_button",
            on_click=add_quick_access_city_handler,
        ),
        Button(
            text=Const(text="Удалить город из быстрого доступа"),
            id="delete_quick_access_city_button",
            on_click=switch_to_remove_quick_access_city_handler,
        ),
        getter=menu_getter,
        state=WeatherSG.menu,
    ),
    Window(
        Format(
            text="🏙<b>{city}</b>\n⏲{time}\n\n🌡Температура: {temperature:.1f}°C\n🤔Ощущается как: {temperature_feels_like:.1f}°C\n🌍Атмосферное давление: {pressure:.1f} мм. рт. ст."
            "\n💧Влажность: {humidity}%\n🍃Скорость ветра: {wind_speed:.1f} м/с"
        ),
        Button(
            text=Const(text="Обновить"),
            id="refresh_button",
            on_click=print_weather_handler,
        ),
        Back(text=Const(text="Назад"), id="back_button"),
        getter=weather_getter,
        state=WeatherSG.weather,
    ),
    Window(
        Const(text="Выберите город(-a) для удаления"),
        Column(
            Multiselect(
                checked_text=Format("[✔️] {item[0]}"),
                unchecked_text=Format("[  ] {item[0]}"),
                id="cities_to_remove",
                item_id_getter=lambda x: x[1],
                items="cities",
            ),
        ),
        Row(
            Button(
                text=Const(text="Подтвердить"),
                id="confirm_remove_from_quick_access",
                on_click=remove_quick_access_city_handler,
            ),
            Button(
                text=Const(text="Отмена"),
                id="discard_changes_button",
                on_click=discard_changes_button_handler,
            ),
        ),
        getter=menu_getter,
        state=WeatherSG.remove_city,
    ),
)
