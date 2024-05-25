from pathlib import Path
from aiogram import Bot
from safe_pass.db.base import DBBase

from .upload import upload_static_files


async def initialize_statics(bot: Bot, 
                        database: DBBase, 
                        chat_id: int,
                        force: bool = False,
                        path: Path = Path("static")):
    if not force and await database.read_statics():
        return
    statics = await upload_static_files(bot, chat_id, path)
    await database.create_statices(statics, force=force)

