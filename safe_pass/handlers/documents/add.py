import json
from aiogram import F, types
from aiogram.fsm.context import FSMContext

from safe_pass.db.base import DBBase
from safe_pass import security
from safe_pass.keyboards.inline import (InlineConstructor,
                                        CANCEL,
                                        USE_MENU,
                                        VIEW_DOCUMENT)
from safe_pass.models.base import User, Document
from safe_pass.states.add_document import AddDocument

from .router import docs_router


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
    m = """<b>2️⃣ Now enter the password: </b>"""
    buttons = [
        CANCEL
    ]
    await state.update_data(title=message.text)
    await state.set_state(AddDocument.data)
    await message.answer(m, reply_markup=InlineConstructor._create_kb(buttons, [1]))


@docs_router.message(AddDocument.data, F.text)
async def set_password(message: types.Message, state: FSMContext, user: User, database: DBBase):
    await message.delete()

    fsm_data = await state.get_data()
    await state.clear()

    if not fsm_data.get('title') or not fsm_data.get('document_pack_identifier'):
        m = """ <b>😞 Something went wrong!</b>
You can try again using /use ."""     
        buttons = [CANCEL]
        await message.answer(m, reply_markup=InlineConstructor._create_kb(buttons, [1, 1]))
        return
        
    data = {"password": message.text}
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
    await message.answer(m, reply_markup=InlineConstructor._create_kb(buttons, [1, 1]))
