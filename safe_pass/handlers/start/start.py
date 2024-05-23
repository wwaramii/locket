from aiogram import types, F
from aiogram.utils import formatting
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.utils.i18n import gettext as _

from safe_pass.keyboards.inline import (NEW_MENU,
                                        USE_MENU,
                                        INFO_MENU,
                                        InlineConstructor)

from .router import start_router


@start_router.message(CommandStart())
async def start_handler(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer(**prepare_answer(message.from_user))


@start_router.callback_query(F.data == "start::start")
async def start_handler_kb(cb: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await cb.message.edit_text(**prepare_answer(cb.from_user))


def prepare_answer(user: types.User):
    m = ("""Welcome {name}👋!
<b>🔒 This is a secure and fast password manager bot. It's easy to use and keeps your data safe.</b>

🪄 Commands:
/start - Main menu
/new - Create a new document pack
/use - Use an existing document pack
/info - Get info about how the bot works
""").format(
    name=formatting.TextMention(user.first_name, user=user).as_html(),
)
    buttons = [
        NEW_MENU,
        USE_MENU,
        INFO_MENU
    ]
    schema = [1, 1, 1]

    return {
        "text": m,
        "reply_markup": InlineConstructor._create_kb(buttons, schema)
    }
