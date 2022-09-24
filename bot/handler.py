import requests
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandStart
from requests.auth import HTTPBasicAuth
from bot.loader import dp
from bot.state import PatientState
from patient.models import Patient


@dp.message_handler(CommandStart(), state='*')
async def send_welcome(message: types.Message):
    await message.reply('🤖 Добро пожаловать\n\n Вас приветсвует помощник системы\n <b>Центра Ортодонтии</b>!',
                        parse_mode=types.ParseMode.HTML)
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton(text="Отправить номер телефона 📱", request_contact=True))
    await message.answer('Для получения доступа отправьте свой контакт\n', reply_markup=keyboard)
    await PatientState.contact.set()


@dp.message_handler(content_types=types.ContentTypes.CONTACT, state=PatientState.contact)
async def search_patient_by_contact(message: types.Message, state: FSMContext):
    contact = message.contact.phone_number.replace('+', '')
    response = requests.get(f'http://127.0.0.1:8000/api/v1/patients/?phone={contact}&chat_id={message.chat.id}',
                            auth=HTTPBasicAuth('admin', 'adminadmin')).json()
    if response:
        await message.answer('✅ Ваш аккаунт успешно прошёл идентификацию!', reply_markup=types.ReplyKeyboardRemove())
    else:
        await message.answer('❌Ваш номер не был зарегистрирован в стоматологии "<b>Центр ортодонтии</b>"',
                             reply_markup=types.ReplyKeyboardRemove(), parse_mode=types.ParseMode.HTML)
    await state.finish()

__all__ = ['dp']
