from typing import Any, Awaitable, Callable, Dict
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from safe_pass.db.base import DBBase

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
        data['database'] = self.database
        return await handler(event, data)
