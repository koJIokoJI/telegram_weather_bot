from logging import Handler
from telebot import TeleBot
from telebot.types import InputFile


class TgHandler(Handler):
    def __init__(self, bot_token: str, chat_id: int):
        Handler.__init__(self)
        if isinstance(chat_id, list | tuple | set | dict):
            raise TypeError(f"A chat_id value must be an integer, not {type(chat_id)}")
        self.bot_token = bot_token
        self.chat_id = chat_id

    def emit(self, record):
        # url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage?text=мы+в+пизде)&chat_id={self.chat_id}"
        # requests.post(url=url)
        photo = InputFile("logs/nu3ga.jpg")
        bot = TeleBot(token=self.bot_token)
        bot.send_photo(
            chat_id=self.chat_id,
            photo=photo,
            caption=f"{record.levelname}: {record.msg}\n{record.pathname}\nLINE: {record.lineno}",
        )
