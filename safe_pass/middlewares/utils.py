from aiogram import types
from aiogram.utils import formatting
from aiogram.fsm.context import FSMContext
from aiogram.utils.i18n import gettext as _

from safe_pass.keyboards import InlineConstructor
from safe_pass.states import SelectLanguage


async def ask_for_language(update: types.Message | types.CallbackQuery,
                           state: FSMContext):
    # define buttons
    buttons = [
        {"text": "🇮🇷 FA", "callback_data": "start::select_lang::FA"},
        {"text": "🇺🇸 EN", "callback_data": "start::select_lang::EN"},
        {"text": "🇷🇺 RU", "callback_data": "start::select_lang::EN"}
    ]
    schema = [1, 1, 1]
    keyboard = InlineConstructor._create_kb(buttons, schema)
    
    # answer
    await update.bot.send_message(chat_id=update.from_user.id,
                                  text=formatting.Bold("🔰 Select Language: ").as_html())
