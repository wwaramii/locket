from aiogram import types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from safe_pass.db.base import DBBase
from safe_pass.keyboards.inline import (InlineConstructor,
                                        CANCEL)
from safe_pass.models.base import User

from .router import pack_router
from .login import start_login


@pack_router.message(Command("use"))
async def use_command(message: types.Message, 
                      database: DBBase, 
                      user: User,
                      state: FSMContext):
    await message.answer(**await use(database, user, state))


@pack_router.callback_query(F.data.startswith("pack::use"))
async def use_cb(cb: types.CallbackQuery, 
                 database: DBBase, 
                 user: User,
                 state: FSMContext):
    # paging
    page = int(cb.data.split("?page=")[-1]) if cb.data.split("?page=")[-1].isnumeric() else 0
    await cb.answer()
    try:
        await cb.message.edit_text(**await use(database, user, state, page=page))
    except:
        pass # paging errors


async def use(database: DBBase, 
              user: User,
              state: FSMContext,
              page: int=0):
    if not user.document_pack:
        return await start_login(state)
    
    m = """<b>🔓 You are logged in and have access to your passwords.</b>
- You will stay logged in for 5 minutes.
- You can logout and access other packs.

<b>📌 All passwords in this pack are listed.</b> You can access each one by tapping it:"""
    # prepare buttons
    buttons = [
        {"text": "➕ Add password", "callback_data": "documents::add"},
        {"text": "🚪 Logout", "callback_data": "pack::logout"}
    ]
    schema = [2]
    
    async for document in database.read_many_docs({
        'document_pack_identifier': user.document_pack.identifier},
        start=page*10,
        end=(page*10) + 10):
        buttons.append({
            "text": f"• {document.title}",
            "callback_data": f"documents::view?id={document.id}"
        })
        schema.append(1)
    buttons.extend([
        {"text": "⬅️ Last page", "callback_data": f"pack::use{page-1}"},
        {"text": "➡️ Next page", "callback_data": f"pack::use?page={page+1}"},
        CANCEL
    ])
    schema.extend([2, 1])

    return {
        "text": m,
        "reply_markup": InlineConstructor._create_kb(buttons, schema)
    }
