import aiogram
import cv2
import os

from aiogram.fsm.storage.memory import MemoryStorage
from keyboards.inlineBuilder import inline_builder
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from aiogram import Router, types
from qreader import QReader
from aiogram import F

router = Router()
storage = MemoryStorage()
qreader = QReader()

class FormStates(StatesGroup):
    waiting_for_img = State()

@router.callback_query(F.data == "read_")
async def start_qr_generation(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text("Пожалуйста, отправьте свою картинку с QR:")
    await state.set_state(FormStates.waiting_for_img)

@router.message(StateFilter(FormStates.waiting_for_img))
async def generate_qr(message: types.Message, state: FSMContext):
    photo = message.photo
    
    if not photo:
        await message.answer("Отправьте картинку с QR!")
    else:
        try:
            file_path = f"{photo[-1].file_id}.jpg"
            await message.bot.download(
                photo[-1],
                destination=file_path
            )

            
            image = cv2.cvtColor(cv2.imread(file_path), cv2.COLOR_BGR2RGB)
            decoded_text = qreader.detect_and_decode(image=image)
            
            
            if decoded_text:  
                qr_data = decoded_text[0] if isinstance(decoded_text, tuple) else decoded_text
                await message.answer(f"Распознанный QR-код содержит данные: {qr_data}", reply_markup=inline_builder("Главное меню", "main_page"))
            else:
                await message.answer("Извините, не удалось распознать QR-код на этой фотографии.", reply_markup=inline_builder("Главное меню", "main_page"))
                
            # Удаляем временный файл после обработки
            os.remove(file_path)

        except Exception as e:
            print(f"Ошибка при обработке изображения: {str(e)}")
            await message.answer("Произошла ошибка при обработке вашего изображения.",reply_markup=inline_builder("Главное меню", "main_page"))

    await state.clear()