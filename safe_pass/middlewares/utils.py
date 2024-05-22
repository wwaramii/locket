from aiogram import types
from aiogram.utils import formatting

from safe_pass.keyboards import InlineConstructor


async def ask_for_language(update: types.Message | types.CallbackQuery):
    # define buttons
    buttons = [
        {"text": "🇷🇺 RU", "callback_data": "select_lang::RU"},
        {"text": "🇺🇸 EN", "callback_data": "select_lang::EN"},
        {"text": "🇮🇷 FA", "callback_data": "select_lang::FA"},
    ]
    schema = [1, 1, 1]
    keyboard = InlineConstructor._create_kb(buttons, schema)
    
    # answer
    await update.bot.send_message(chat_id=update.event.from_user.id,
                                  text=formatting.Bold("🔰 Select Language: ").as_html(),
                                  reply_markup=keyboard)
