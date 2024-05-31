from typing import Dict
from aiogram import types, F
from aiogram.filters import Command

from safe_pass.keyboards.inline import (NEW_MENU,
                                        USE_MENU,
                                        MAIN_MENU,
                                        InlineConstructor)

from .router import info_router

from aiogram.utils.i18n import gettext as _


@info_router.message(Command("info"))
async def info(message: types.Message):
    await message.answer(**prepare_info())


@info_router.callback_query(F.data == "info::info")
async def info_cb(cb: types.CallbackQuery):
    await cb.message.edit_text(**prepare_info())


def prepare_info() -> Dict:
    m = _("""<b>🔒 Locket</b> is the <b>safest</b> and <b>smoothest</b> password manager on Telegram.

🔰 <b>Locket</b> ensures your passwords are always secure and accessible only by you. 
Here’s how we do it:

🔹 <b>Encrypted data:</b> No raw passwords are stored.
🔹 <b>Owner-only access:</b> Only the data owner can access their information.
🔹 <b>Anonymized data:</b> It's impossible to determine which data belongs to which user.
🔹 <b>Open source:</b> <b>Locket</b> is fully transparent and <a href="https://github.com/wwaramii/locket">open source</a>.

✅ Your data is completely safe.

🔰 Start using Locket by creating a new password pack with the /new command. Keep your secret phrase safe, and access or store all your secrets with /use.

🖤 Enjoy Locket!
""")
    buttons = [
        MAIN_MENU,
        NEW_MENU,
        USE_MENU]
    

    return {
        "text": m,
        "reply_markup": InlineConstructor._create_kb(buttons, [1, 1, 1])
    }
