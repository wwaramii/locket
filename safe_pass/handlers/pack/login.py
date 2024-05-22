from aiogram.fsm.context import FSMContext
from aiogram import types, F

from safe_pass.db import DBBase, DocumentNotFoundError
from safe_pass.models.base import User
from safe_pass.keyboards import InlineConstructor
from safe_pass import security
from safe_pass.states.login import Login

from .router import pack_router


async def start_login(state: FSMContext):
    m = ("""<b>🔐 To access a document pack, please enter its secret key.</b>
You'll gain access to all passwords stored in the pack.

<b>Enter the secret phrase:</b>
""")
    
    buttons = [
        {"text": "🔙 Cancel", "callback_data": "globals::cancel"}
    ]

    await state.set_state(Login.secret_key)
    
    return {
        "text": m,
        "reply_markup": InlineConstructor._create_kb(buttons, [1]) 
    }


@pack_router.message(Login.secret_key, F.text)
async def login_with_secret_key(message: types.Message,
                                state: FSMContext,
                                user: User,
                                database: DBBase):
    secret_key = message.text
    # delete the message
    await message.delete()
    identifier = security.generate_identifier(str(user.user_id), secret_key)
    try:
        doc_pack = await database.read_one_doc_pack(dict(identifier=identifier))
        user.document_pack = doc_pack
        user.key = security.generate_key(doc_pack.identifier,
                                         str(user.user_id),
                                         secret_key)
        await database.update_user(dict(user_id=user.user_id), user)
        await state.clear()
        m = """<b>You successfully logged in! 🎉</b>

You can now access all passwords stored in this pack with /use. <b>You will stay logged in for 5 minutes.</b>

<b>🔒 Enjoy your secure experience!</b>"""
        buttons = [
            {"text": "• New | Create new pack", "callback_data": "pack::new"},
            {"text": "• Use | Use available pack", "callback_data": "pack::use"}
        ]
        await message.answer(m,
                             reply_markup=InlineConstructor._create_kb(buttons, [1, 1]))
    except DocumentNotFoundError:
        await state.clear()
        m = """<b>❗️ Invalid secret key. Please try again /use.</b>"""
        await message.answer(m)
