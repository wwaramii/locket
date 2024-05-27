from aiogram import F, types
from aiogram.utils import formatting
from aiogram.fsm.context import FSMContext

from safe_pass.db.base import DBBase
from safe_pass.models import User

from .router import pack_router


@pack_router.callback_query(F.data == "pack::logout")
async def logout(cb: types.CallbackQuery, user: User, database: DBBase, state: FSMContext):
    await state.clear()
    user.document_pack = None
    user.key = None
    await database.update_user({'user_id': user.user_id}, user)
    await cb.message.edit_text(formatting.BlockQuote("Logged out...").as_html())
