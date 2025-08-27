from aiohttp import ClientSession
from datetime import datetime, timezone, timedelta


class Weather:
    def __init__(
        self,
        time_zone: int,
        temperature: float,
        temperature_feels_like: float,
        pressure: float,
        humidity: float,
        wind_speed: float,
    ):
        KELVIN = -273.15
        HPA = 133.322
        self.time = datetime.now(timezone(timedelta(hours=time_zone // 3600))).strftime(
            "%d.%m.%Y | %H:%M:%S"
        )
        self.temperature = temperature
        self.temperature_in_celsius = temperature + KELVIN
        self.temperature_feels_like = temperature_feels_like
        self.temperature_feels_like_in_celsius = temperature_feels_like + KELVIN
        self.pressure = pressure
        self.pressure_in_mmrtst = pressure / (HPA / 10**2)
        self.humidity = humidity
        self.wind_speed = wind_speed


async def get_weather(city: str, token: str) -> Weather:
    return await get_json(get_url(city=city, token=token))


def get_url(city: str, token: str) -> str:
    return f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={token}"


async def get_json(url: str) -> dict:
    async with ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                return get_weather_from_json(await response.json())


def get_weather_from_json(json: dict) -> Weather:
    time_zone = json["timezone"]
    temperature = json["main"]["temp"]
    temperature_feels_like = json["main"]["feels_like"]
    pressure = json["main"]["pressure"]
    humidity = json["main"]["humidity"]
    wind_speed = json["wind"]["speed"]
    return Weather(
        time_zone=time_zone,
        temperature=temperature,
        temperature_feels_like=temperature_feels_like,
        pressure=pressure,
        humidity=humidity,
        wind_speed=wind_speed,
    )
