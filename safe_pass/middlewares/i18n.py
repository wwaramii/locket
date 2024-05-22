from aiogram.utils.i18n.middleware import I18nMiddleware
from typing import Any, Dict, Tuple
from aiogram.types import Message, CallbackQuery

from .utils import ask_for_language
from safe_pass.models import User


class CustomI18nMiddleware(I18nMiddleware):
    async def get_locale(self, event: Message | CallbackQuery, 
                         data: Dict[str, Any]) -> str:
        try:
            user: User = data['user']
            if not user.language:
                await ask_for_language(update=event)
                return         
        except KeyError:
            raise KeyError("You should first initialize database middleware.")    

        return user.language.value
