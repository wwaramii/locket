from aiogram import F, types

from .router import global_router
from .utils import delete_message


@global_router.callback_query(F.data == "globals::delete_message")
async def delete_message_cb(cb: types.CallbackQuery):
    await delete_message(cb.message)
