from datetime import datetime, timedelta
from typing import Any, Awaitable, Callable, Dict
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message, CallbackQuery

from safe_pass.keyboards.inline import InlineConstructor, NEW_MENU, USE_MENU
from safe_pass.db import DBBase
from safe_pass.models import User

from aiogram.utils.i18n import gettext as _


class LoginRequiredMiddleware(BaseMiddleware):
    async def __call__(self, 
                        handler: Callable[[TelegramObject, Dict[str, Any]], 
                        Awaitable[Any]], 
                        event: TelegramObject, 
                        data: Dict[str, Any]) -> Any:
        try:
            user: User = data['user']
            database: DBBase = data['database']
        except KeyError:
            raise KeyError("You should first initialize database middleware.")
    
        if user.document_pack and user.key and self.__check_last_login(user):
            return await handler(event, data)
        else:
            # make sure document_pack & key are both none
            user.document_pack = None
            user.key = None
            user.last_login = None
            await database.update_user({'user_id': user.user_id}, user)
            # send answer to user
            if isinstance(event, Message):
                await event.answer(**self.__prepare_answer())
            elif isinstance(event, CallbackQuery):
                await event.message.edit_text(**self.__prepare_answer())   
            return None
        
    def __check_last_login(self, user: User) -> bool:
        """
        Use user.last_login to check if it's more than 5 minuets ago.
        If user can stay logged in, return True.
        """
        if datetime.now(user.last_login.tzinfo) - user.last_login > timedelta(minutes=5):
            return False
        return True

    def __prepare_answer(self):
        m = _("""<b>❗️ You are not logged in!</b>
With /use you can login and access your passwords.""")
        buttons = [
            NEW_MENU,
            USE_MENU,
        ]
        schema = [1, 1]

        return {
            'text': m,
            'reply_markup': InlineConstructor._create_kb(buttons, schema)
        }
