import asyncio
from aiogram import types

async def delete_message(message: types.Message,
                         delay: int = 0):
    try:
        await asyncio.sleep(delay)
        await message.delete()
    except Exception as ex:
        print(f"[!] Could not delete message after {delay} seconds: {ex}")
    