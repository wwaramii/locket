import asyncio
import logging
from safe_pass.db.storages.panther import Panther
from safe_pass.models.base import User
from .config import config
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from safe_pass.middlewares import DatabaseMiddleware

def initialize_logging():
    logging.basicConfig(level=logging.DEBUG)


def main():
    # logging
    initialize_logging()
    
    # initialize bot
    bot = Bot(token=config["bot"]["TOKEN"],
              default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()

    # initialize database
    database = Panther()
    
    dp.update.middleware(DatabaseMiddleware(database))
    # add routers

    # start polling
    asyncio.run(dp.start_polling(bot))


if __name__ == "__main__":
    main()
