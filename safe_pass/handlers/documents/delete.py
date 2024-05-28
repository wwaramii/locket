from aiogram import F, types
from aiogram.fsm.context import FSMContext

from safe_pass.db import DBBase, CouldNotDelete, DocumentNotFoundError
from safe_pass.keyboards.inline import (InlineConstructor,
                                        USE_MENU,
                                        MAIN_MENU,
                                        NEW_MENU)
from safe_pass.models import User

from .router import docs_router

from aiogram.utils.i18n import gettext as _


@docs_router.callback_query(F.data.startswith("documents::delete?id="))
async def view_document(cb: types.CallbackQuery, user: User, database: DBBase, state: FSMContext):
    await state.clear()    
    # check it's a valid callback
    doc_id = cb.data.split("id=")[-1] if len(cb.data.split("id=")) != 1 else None
    if not doc_id:
        await cb.message.delete()
        return

    try:
        doc = await database.read_one_doc({'id': doc_id})
        if doc.document_pack_identifier != user.document_pack.identifier:
            m = _("""<b>❗ You are not logged in or you don't have access to this password.</b>
You can simply login with /use and access your stored passwords.
Or you can create a  pack for storing your password with  /new .""")
            buttons = [NEW_MENU, USE_MENU]
            schema = [1, 1]
            await cb.message.edit_text(m, reply_markup=InlineConstructor._create_kb(buttons, schema))
            return

        # delete
        await database.delete_doc({'id': doc_id})
        m = _(f"""<b>✅ Your password </b><i>{doc.title}</i> <b>was successfully deleted.</b>""")
        buttons = [MAIN_MENU]
        schema = [1]
        await cb.answer()
        await cb.message.edit_text(m, 
                                reply_markup=InlineConstructor._create_kb(buttons, schema))
    
    except (CouldNotDelete, DocumentNotFoundError):
        # if the doc id is invalid
        m = _("""<b>❗ We wasn't able to delete your password.</b>""")
        buttons = [MAIN_MENU, USE_MENU]
        schema = [1, 1]
        await cb.message.edit_text(m, reply_markup=InlineConstructor._create_kb(buttons, schema))

    except Exception as ex:
        # if the doc id is invalid
        m = _("""<b>🤔 Something was'nt right.</b>
Logout with /use and re-login to fix the issue or contact support.""")
        buttons = [MAIN_MENU, USE_MENU]
        schema = [1, 1]
        await cb.message.edit_text(m, reply_markup=InlineConstructor._create_kb(buttons, schema))
