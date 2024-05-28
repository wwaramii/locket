from aiogram import F, types
from aiogram.fsm.context import FSMContext
from aiogram.utils import formatting

from .router import global_router

from aiogram.utils.i18n import gettext as _

@global_router.callback_query(F.data == "globals::cancel")
async def cancel(cb: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await cb.message.edit_text(formatting.BlockQuote(_("Operation canceled...")).as_html())
