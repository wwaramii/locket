import json
from typing import Dict
from aiogram import F, types
from aiogram.fsm.context import FSMContext

from safe_pass.db.base import DBBase
from safe_pass import security
from safe_pass.keyboards.inline import (InlineConstructor,
                                        CANCEL,
                                        USE_MENU,
                                        VIEW_DOCUMENT, 
                                        GENERATE_PASSWORD)
from safe_pass.models import User, Document
from safe_pass.states.add_document import AddDocument

from .router import docs_router
from .utils import generate_password


@docs_router.callback_query(F.data=="documents::add")
async def start_add(cb: types.CallbackQuery, 
                    state: FSMContext,
                    user: User):
    m = """<b>1️⃣ Please enter a title for the password: </b>"""
    buttons = [
        CANCEL,
        USE_MENU
    ]
    await state.clear()
    await state.update_data(document_pack_identifier=user.document_pack.identifier)
    await state.set_state(AddDocument.title)
    await cb.message.edit_text(m, reply_markup=InlineConstructor._create_kb(buttons, [1, 1]))


@docs_router.message(AddDocument.title, F.text)
async def set_title(message: types.Message, state: FSMContext):
    # check for length
    if len(message.text) > 45:
        m = """<b>❗ This title is too long(max 45 characters).</b>

1️⃣ Re-enter a <b>shorter</b> password: """
        buttons = [CANCEL, USE_MENU]
        await message.answer(m, reply_markup=InlineConstructor._create_kb(buttons, [1, 1]))
        return
    
    m = """<b>2️⃣ Now enter the password: </b>"""
    buttons = [
        GENERATE_PASSWORD,
        CANCEL
    ]
    await state.update_data(title=message.text)
    await state.set_state(AddDocument.data)
    await message.answer(m, reply_markup=InlineConstructor._create_kb(buttons, [1,1 ]))


@docs_router.message(AddDocument.data, F.text)
async def get_password(message: types.Message, state: FSMContext, user: User, database: DBBase):
    d = await set_data(fsm_data=await state.get_data(),
                       password=message.text,
                       user=user,
                       database=database)
    await state.clear()
    await message.delete()
    await message.answer(**d)


@docs_router.callback_query(F.data == "documents::add::generate_password")
async def get_password_kb(cb: types.CallbackQuery, state: FSMContext, user: User, database: DBBase):
    d = await set_data(fsm_data=await state.get_data(),
                       password=generate_password(12),
                       user=user,
                       database=database)
    await state.clear()
    await cb.message.edit_text(**d)


async def set_data(fsm_data: Dict,
                   password: str,
                   user: User, 
                   database: DBBase):
    if not fsm_data.get('title') or not fsm_data.get('document_pack_identifier'):
        m = """ <b>😞 Something went wrong!</b>
You can try again using /use ."""     
        buttons = [CANCEL]
        schema = [1]
    else:        
        data = {"password": password}
        # encrypt data
        data = security.encrypt_document(json.dumps(data), user.key).hex()
        # save to db
        doc = Document(document_pack_identifier=fsm_data['document_pack_identifier'],
                    title=fsm_data['title'],
                    encrypted_data=data)
        doc = await database.create_document(doc)
        # answer
        m = """<b>Password was safely added to the pack🎉</b>
You can access it threw /use or the below button..
    """
        buttons = [
            VIEW_DOCUMENT(doc.title, doc.id),
            USE_MENU
        ]
        schema = [1, 1]
    
    return {
        "text": m,
        "reply_markup": InlineConstructor._create_kb(buttons, schema)
    }
