from datetime import datetime
from aiogram.fsm.context import FSMContext
from aiogram import types, F

from safe_pass.db import DBBase, DocumentNotFoundError
from safe_pass.models import User
from safe_pass.keyboards.inline import (InlineConstructor, 
                                        MAIN_MENU, 
                                        USE_MENU,
                                        CANCEL)
from safe_pass import security
from safe_pass.states.login import Login

from .router import pack_router


async def start_login(state: FSMContext):
    m = ("""<b>🔐 To access a document pack, please enter its secret key.</b>
You'll gain access to all passwords stored in the pack.

<b>Enter the secret phrase:</b>
""")
    
    buttons = [
        CANCEL,
        MAIN_MENU
    ]

    await state.set_state(Login.secret_key)
    
    return {
        "text": m,
        "reply_markup": InlineConstructor._create_kb(buttons, [1, 1]) 
    }


@pack_router.message(Login.secret_key, F.text)
async def login_with_secret_key(message: types.Message,
                                state: FSMContext,
                                user: User,
                                database: DBBase):
    await state.clear()
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
        user.last_login = datetime.now()
        await database.update_user(dict(user_id=user.user_id), user)
        m = """<b>You successfully logged in! 🎉</b>

You can now access all passwords stored in this pack with /use. <b>You will stay logged in for 5 minutes.</b>

<b>🔒 Enjoy your secure experience!</b>"""
        buttons = [
            MAIN_MENU,
            USE_MENU
        ]
        await message.answer(m,
                             reply_markup=InlineConstructor._create_kb(buttons, [1, 1]))
    except DocumentNotFoundError:
        m = """<b>❗️ Invalid secret key. Please try again /use.</b>"""
        await message.answer(m)
