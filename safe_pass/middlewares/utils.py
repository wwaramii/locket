from aiogram import types
from aiogram.utils import formatting

from safe_pass.db.base import DBBase
from safe_pass.keyboards import InlineConstructor
from safe_pass.models import User, Languages


async def ask_for_language(event: types.Message | types.CallbackQuery):
    # define buttons
    buttons = [
        {"text": "🇷🇺 RU", "callback_data": "select_lang::RU"},
        {"text": "🇺🇸 EN", "callback_data": "select_lang::EN"},
        {"text": "🇮🇷 FA", "callback_data": "select_lang::FA"},
    ]
    schema = [1, 1, 1]
    keyboard = InlineConstructor._create_kb(buttons, schema)
    
    # answer
    await event.bot.send_message(chat_id=event.from_user.id,
                                  text=formatting.Bold("🔰 Select Language: ").as_html(),
                                  reply_markup=keyboard)

async def set_language(database: DBBase,
                       user: User,
                       lang: str,
                       event: types.CallbackQuery):
        user.language = Languages(lang.lower())
        await database.update_user({"user_id": user.user_id}, user)
        await event.answer("✅")
        await event.message.delete()
