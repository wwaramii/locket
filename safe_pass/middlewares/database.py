from typing import Any, Awaitable, Callable, Dict
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from safe_pass.db import DBBase, DocumentNotFoundError
from safe_pass.models import User


class DatabaseMiddleware(BaseMiddleware):
    """
    this middleware will pass each handler the initialized database as an argument.
    """
    def __init__(self, database: DBBase) -> None:
        self.database = database
        super().__init__()
    
    async def __call__(self, 
                        handler: Callable[[TelegramObject, 
                        Dict[str, Any]], Awaitable[Any]], 
                        event: TelegramObject, 
                        data: Dict[str, Any]) -> Any:
        # initialize user
        try:
            user: User = await self.database.read_one_user(dict(user_id=event.event.from_user.id))   
        except DocumentNotFoundError:
            user: User = await self.database.create_user(User(user_id=event.event.from_user.id))
        # update arguments
        data['database'] = self.database
        data['user'] = user
        return await handler(event, data)
