import qrcode
import os

from aiogram.types import InputMediaPhoto, BufferedInputFile
from aiogram.filters import CommandStart, StateFilter
from aiogram.fsm.storage.memory import MemoryStorage
from keyboards.inlineBuilder import inline_builder
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram import Router, types
from aiogram import F
from io import BytesIO



router = Router()
storage = MemoryStorage()

class FormStates(StatesGroup):
    waiting_for_url = State()

@router.callback_query(F.data == "gen_")
async def start_qr_generation(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text("Пожалуйста, отправьте свою ссылку для генерации QR-кода:")
    await state.set_state(FormStates.waiting_for_url)

@router.message(StateFilter(FormStates.waiting_for_url))
async def generate_qr(message: types.Message, state: FSMContext):
    url: str = message.text  

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=3,
    )
    
    qr.add_data(url)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    buffer = BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)

    try:
        photo_file = BufferedInputFile(buffer.getvalue(), filename="qrcode.png")
        await message.answer_photo(photo=photo_file, caption=f"Ваш QR-код для {url} сгенерирован!")
        await message.answer("Portal", reply_markup=inline_builder("Главное меню", "main_page"))
    except Exception as e:
        print(f"Ошибка при отправке изображения: {str(e)}")
        await message.answer("Извините, произошла ошибка при отправке QR-кода.", reply_markup=inline_builder("Главное меню", "main_page"))

    await state.clear()