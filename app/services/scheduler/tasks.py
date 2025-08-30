from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums.parse_mode import ParseMode
from taskiq import TaskiqScheduler
from taskiq_nats import NatsBroker
from taskiq.schedule_sources import LabelScheduleSource
from taskiq_redis import RedisScheduleSource

from app.services.weather_service import Weather, get_weather
from config.config import settings

broker = NatsBroker(servers=settings.nats_servers, queue="mailing_weather_queue")
redis_source = RedisScheduleSource(
    url=f"redis://{settings.redis_host}:{settings.redis_port}"
)
scheduler = TaskiqScheduler(
    broker=broker, sources=[redis_source, LabelScheduleSource(broker)]
)


@broker.task(schedule=[{"cron": "*/1 * * * *"}])
async def periodic_task():
    bot = Bot(
        token=settings.bot_token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    city = "Красноярск"
    weather: Weather = await get_weather(city=city, token=settings.open_weather_token)
    text = "🏙<b>{city}</b>\n⏲{time}\n\n🌡Температура: {temperature:.1f}°C\n🤔Ощущается как: {temperature_feels_like:.1f}°C\n🌍Атмосферное давление: {pressure:.1f} мм. рт. ст.\n💧Влажность: {humidity}%\n🍃Скорость ветра: {wind_speed:.1f} м/с".format(
        city=city,
        time=weather.time,
        temperature=weather.temperature_in_celsius,
        temperature_feels_like=weather.temperature_feels_like_in_celsius,
        pressure=weather.pressure_in_mmrtst,
        humidity=weather.humidity,
        wind_speed=weather.wind_speed,
    )
    await bot.send_message(
        chat_id=788266502,
        text=text,
    )

    return await bot.session.close()
