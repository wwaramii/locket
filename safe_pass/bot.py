import asyncio
import logging

from aiogram.client.default import DefaultBotProperties
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.utils.i18n import I18n

from safe_pass.config import config
from safe_pass.db.storages.panther import Panther
from safe_pass.middlewares import DatabaseMiddleware, CustomI18nMiddleware

from safe_pass.handlers import start_router, pack_router, global_router


def initialize_logging():
    logging.basicConfig(level=logging.DEBUG)


def main():
    # i18n
    i18n = I18n(path="locales", default_locale="en", domain="messages")

    # logging
    initialize_logging()

    # use proxy
    session = None
    if config['proxy']['address']:
        session = AiohttpSession(proxy=config['proxy']['address'])
    
    # initialize bot
    bot = Bot(token=config["bot"]["TOKEN"],
              session=session,
              default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()

    # initialize database
    database = Panther()
    
    # middlewares
    dp.update.middleware(DatabaseMiddleware(database))
    dp.update.middleware(CustomI18nMiddleware(i18n))
    
    # add routers
    dp.include_router(global_router)
    dp.include_router(start_router)
    dp.include_router(pack_router)

    # start polling
    asyncio.run(dp.start_polling(bot))


if __name__ == "__main__":
    main()
