from aiogram.utils.i18n.middleware import I18nMiddleware
from aiogram.types import Message, CallbackQuery
from aiogram.types import TelegramObject

from typing import Any, Dict, Tuple
from typing import Any, Awaitable, Callable, Dict

from .utils import ask_for_language, set_language
from safe_pass.models import User
from safe_pass.db import DBBase
from safe_pass.handlers.start.start import start_handler_kb

class CustomI18nMiddleware(I18nMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        is_new, current_locale = await self.get_locale(event=event, data=data)
        if not current_locale:
            return 
        
        if self.i18n_key:
            data[self.i18n_key] = self.i18n
        if self.middleware_key:
            data[self.middleware_key] = self

        with self.i18n.context(), self.i18n.use_locale(current_locale):
            if is_new:
                return await start_handler_kb(event.event, **data)
            return await handler(event, data)
        
    async def get_locale(self, event: Message | CallbackQuery, 
                         data: Dict[str, Any]) -> Tuple[bool, str] | None:
        try:
            user: User = data['user']
            database: DBBase = data['database']
            # check for updating the user lang
            if isinstance(event.event, CallbackQuery) and event.event.data.startswith("select_lang::"):
                lang = event.event.data.split("::")[-1]
                return True, await set_language(database, user, lang, event.event)

            # ask for user lang
            if not user.language:
                await ask_for_language(event=event.event)
                return None, None
                         
        except KeyError:
            raise KeyError("You should first initialize database middleware.")    

        return False, user.language.value
