from aiogram import types, F
from aiogram.utils import formatting
from aiogram.filters import Command
from typing import Dict
from aiogram.utils.i18n import gettext as _

from safe_pass.db.base import DBBase
from safe_pass.keyboards import InlineConstructor
from safe_pass.models.base import User, DocumentPack
from safe_pass import security
from safe_pass.handlers.globals import utils

from .router import pack_router


@pack_router.message(Command("new"))
async def new_command(message: types.Message, database: DBBase, user: User):
    secret_key = await create_pack(user, database)

    m = await message.answer(**prepare_answer(secret_key))
    await utils.delete_message(m, delay=120)


@pack_router.callback_query(F.data == "pack::new")
async def new_cb(cb: types.CallbackQuery, database: DBBase, user: User):
    secret_key = await create_pack(user, database)

    await cb.message.edit_text(**prepare_answer(secret_key))
    await utils.delete_message(cb.message, delay=120)


async def create_pack(user: User, database: DBBase) -> str:
    # generate a secret phrase
    secret_phrase = security.generate_secret_phrase()
    # generate pack identifier
    identifier = security.generate_identifier(str(user.user_id), secret_phrase)
    # create the document pack
    doc_pack = DocumentPack(identifier=identifier)
    await database.create_doc_pack(doc_pack)

    return secret_phrase


def prepare_answer(secret_key: str) -> Dict:
    m = ("""<b>Pack created! 🎉</b>

You can now store your passwords securely. Remember to keep your secret key safe, as it's the only way to access your pack. <b>Without it, your passwords are lost.</b>

⛔️ <b>Secret key:</b> {secret_key}
         
🕑 This message will be deleted after <b>2 minutes</b>.
""").format(
    secret_key=formatting.Code(secret_key).as_html()
)
    buttons = [
        {"text": "❌ Delete Now!", "callback_data": "globals::delete_message"},
        {"text": "🔙 Main menu", "callback_data": "start::start"}
    ]
    return {
        "text": m,
        "reply_markup": InlineConstructor._create_kb(buttons, [1, 1])
    }
