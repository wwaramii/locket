from aiogram import types
from aiogram.utils import formatting
from aiogram.filters import CommandStart
from aiogram.utils.i18n import gettext as _

from safe_pass.keyboards import InlineConstructor

from .router import start_router

@start_router.message(CommandStart())
async def start_handler(message: types.Message, **kwargs):
    m = ("""Welcome {name}👋!
<b>🔒 This is a secure and fast password manager bot. It's easy to use and keeps your data safe.</b>

🪄 Commands:
/start - Main menu
/new - Create a new document pack
/use - Use an existing document pack
/info - Get info about how the bot works
""").format(
    name=formatting.TextMention(message.from_user.first_name, user=message.from_user).as_html(),
)
    buttons = [
        {"text": "• New | Create new pack", "callback_data": "pack::new"},
        {"text": "• Use | Use available pack", "callback_data": "pack::use"},
        {"text": "• Info | How am I safe here?", "callback_data": "global::description"},
    ]
    schema = [1, 1, 1]

    await message.answer(m,
                         reply_markup=InlineConstructor._create_kb(buttons, schema))

    