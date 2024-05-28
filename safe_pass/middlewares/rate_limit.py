import time
from collections import defaultdict
from typing import Any, Awaitable, Callable, Dict
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Update

from aiogram.utils.i18n import gettext as _


class RateLimitMiddleware(BaseMiddleware):
    def __init__(self, limit: int=100, time_window: int=60) -> None:
        self.limit = limit
        self.time_window = time_window
        self.user_requests = defaultdict(list)
        super().__init__()
    
    async def __call__(self, 
                       handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]], 
                       event: Update, 
                       data: Dict[str, Any]) -> Any:
        user_id = event.event.from_user.id
        current_time = time.time()
        
        # Filter out old requests
        self.user_requests[user_id] = [
            timestamp for timestamp in self.user_requests[user_id]
            if current_time - timestamp < self.time_window
        ]

        
        # Check if user is over the limit
        if len(self.user_requests[user_id]) >= self.limit:
            m = ("""<b>⛔️ Too many requests!</b>
You might have to <b>wait a minute</b> to start using it again.

<b>🌟 You can get /vip account for no limitations. </b>
""")       
            await event.bot.send_message(chat_id=event.event.from_user.id,
                                         text=m)
            self.user_requests[user_id].append(current_time)
            return
        
        # Record the current request
        self.user_requests[user_id].append(current_time)
        return await handler(event, data)
