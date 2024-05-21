import asyncio
import logging
from .config import config
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode


def initialize_logging():
    logging.basicConfig(level=logging.DEBUG)


def main():
    # logging
    initialize_logging()
    # telegram bot
    bot = Bot(token=config["bot"]["TOKEN"],
              default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()
    # add routers

    # start polling
    asyncio.run(dp.start_polling(bot))


if __name__ == "__main__":
    asyncio.run(main())
