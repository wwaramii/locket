import json
from aiogram import F, types
from aiogram.fsm.context import FSMContext

from safe_pass.db import DBBase, DocumentNotFoundError
from safe_pass import security
from safe_pass.keyboards.inline import (InlineConstructor,
                                        DELETE_NOW,
                                        USE_MENU,
                                        MAIN_MENU,
                                        NEW_MENU)
from safe_pass.models.base import User
from safe_pass.handlers.globals import utils

from .router import docs_router


@docs_router.callback_query(F.data.startswith("documents::view?id="))
async def view_document(cb: types.CallbackQuery, user: User, database: DBBase, state: FSMContext):
    await state.clear()
    # check user is logged in
    if not user.key:
        m = """<b>❗ You are not logged in!</b>
You can simply login with /use and access your stored passwords.
Or you can create a  pack for storing your password with  /new .
""" 
        buttons = [NEW_MENU, USE_MENU]
        schema = [1, 1]
        await cb.message.edit_text(m, reply_markup=InlineConstructor._create_kb(buttons, [1, 1]))
        return

    # check it's a valid callback
    doc_id = cb.data.split("id=")[-1] if len(cb.data.split("id=")) != 1 else None
    if not doc_id:
        await cb.message.delete()
        return

    try:
        doc = await database.read_one_doc({'id': doc_id})
        data = security.decrypt_document(bytes.fromhex(doc.encrypted_data),
                                         user.key)
        data: dict = json.loads(data)

        fields = [f"<b>{key.title()}:</b> <code>{value}</code>" for key, value in data.items()]
        m = ("""<b>🔑 Your stored password:</b>
             
<b>📌 Title:</b> {title}
{fields}

🕑 This message will be deleted after <b>1 minute</b>.""").format(
    title=doc.title,
    fields='\n'.join(fields)
)
        buttons = [DELETE_NOW]
        schema = [1]
        await cb.answer()
        ms = await cb.message.answer(m, reply_markup=InlineConstructor._create_kb(buttons, schema))
        await utils.delete_message(ms, delay=60)
        
    except DocumentNotFoundError:
        # if the doc id is invalid
        m = """<b>❗ Try accessing your password threw /use.</b>"""
        buttons = [MAIN_MENU, USE_MENU]
        schema = [1, 1]
        await cb.message.edit_text(m, reply_markup=InlineConstructor._create_kb(buttons, schema))

    except Exception as ex:
        # if the doc id is invalid
        m = """<b>🤔 Something was'nt right.</b>
Logout with /use and re-login to fix the issue or contact support."""
        buttons = [MAIN_MENU, USE_MENU]
        schema = [1, 1]
        await cb.message.edit_text(m, reply_markup=InlineConstructor._create_kb(buttons, schema))
