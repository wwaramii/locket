from aiogram import Bot, types
from pathlib import Path
from safe_pass.models.statics import Statics

async def upload_static_files(bot: Bot, 
                              chat_id: int,
                              path: Path = Path("static")) -> Statics:
    """
    This will upload all static files in the 'images' subfolder
    and return a dictionary mapping file names to their respective file_ids.
    TODO: add other file types(gif, webp...)
    """
    statics = Statics(images={})
    images = path / "images"

    if not images.exists():
        return statics

    for image_file in images.iterdir():
        if image_file.is_file():
            photo = types.FSInputFile(image_file)
            sent_photo = await bot.send_photo(chat_id=chat_id, photo=photo)
            file_id = sent_photo.photo[-1].file_id
            statics.images[image_file.name.split(".")[0]] = file_id

    return statics
