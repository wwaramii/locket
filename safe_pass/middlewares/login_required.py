from typing import Any, Awaitable, Callable, Dict
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message, CallbackQuery

from safe_pass.keyboards import InlineConstructor
from safe_pass.db import DBBase
from safe_pass.models import User


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
        
        if not user.document_pack or not user.key:
            # make sure document_pack & key are both none
            user.document_pack = None
            user.key = None
            await database.update_user({'user_id': user.user_id}, user)
            # send answer to user
            if isinstance(event, Message):
                await event.answer(**self.__prepare_answer())
            elif isinstance(event, CallbackQuery):
                await event.message.edit_text(**self.__prepare_answer())   
            return None
        
        return await handler(event, data)

    def __prepare_answer(self):
        m = """<b>❗️ You are not logged in!</b>
With /use you can login and access your passwords."""
        buttons = [
            {"text": "• New | Create new pack", "callback_data": "pack::new"},
            {"text": "• Use | Use available pack", "callback_data": "pack::use"},
        ]
        schema = [1, 1]

        return {
            'text': m,
            'reply_markup': InlineConstructor._create_kb(buttons, schema)
        }
