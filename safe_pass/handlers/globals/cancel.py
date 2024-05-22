from aiogram import F, types
from aiogram.fsm.context import FSMContext
from aiogram.utils import formatting

from .router import global_router


@global_router.callback_query(F.data == "globals::cancel")
async def cancel(cb: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await cb.message.edit_text(formatting.BlockQuote("Operation canceled...").as_html())
