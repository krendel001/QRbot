import asyncio
import aiogram
import logging

from routers.user_commands import storage
from aiogram import Bot, Dispatcher
from routers import user_commands
from routers import qr_generation
from routers import decode_qrcode

API_TOKEN = 'TOKEN'

bot = Bot(token=API_TOKEN)
dp = Dispatcher(storage=storage)

async def start_bot():
    dp.include_routers(
        user_commands.router,
        qr_generation.router,
        decode_qrcode.router
    )
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())



if __name__ == "__main__":
    asyncio.run(start_bot())