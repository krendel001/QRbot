import qrcode
from io import BytesIO
import os

from aiogram import F
from aiogram import Router, types
from aiogram.filters import CommandStart, StateFilter
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from keyboards.inlineBuilder import inline_builder
from aiogram.types import InputMediaPhoto, BufferedInputFile



router = Router()
storage = MemoryStorage()

@router.message(CommandStart())
@router.callback_query(F.data == "main_page")
async def start(message: types.Message | types.CallbackQuery):

    pattern = {
        "text": f"Привет! Тут ты можешь сгенерировать QR код абсолютно бесплатно!",
        "reply_markup": inline_builder(["Сгенерировать", "Отсканировать"], ["gen_", "read_"])
    }

    if isinstance(message, types.CallbackQuery):
        await message.message.edit_text(**pattern, parse_mode="HTML")
        await message.answer()
    else:
        await message.answer(**pattern, parse_mode="HTML")