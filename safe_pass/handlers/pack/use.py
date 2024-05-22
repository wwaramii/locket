from aiogram import types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from safe_pass.db.base import DBBase
from safe_pass.keyboards import InlineConstructor
from safe_pass.models.base import User

from .router import pack_router
from .login import start_login

@pack_router.message(Command("use"))
async def use_command(message: types.Message, 
                      database: DBBase, 
                      user: User,
                      state: FSMContext):
    await message.answer(**await use(database, user, state))
    ...


@pack_router.callback_query(F.data == "pack::use")
async def use_cb(cb: types.CallbackQuery, 
                 database: DBBase, 
                 user: User,
                 state: FSMContext):
    await cb.message.edit_text(**await use(database, user, state))


async def use(database: DBBase, 
              user: User,
              state: FSMContext):
    if not user.document_pack:
        return await start_login(state)
    # TODO: handle using a document
