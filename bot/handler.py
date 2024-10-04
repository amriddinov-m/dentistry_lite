import requests
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandStart
from aiogram.types import WebAppInfo
from requests.auth import HTTPBasicAuth
from bot.loader import dp
from bot.state import PatientState
from patient.models import Patient


@dp.message_handler(CommandStart(), state='*')
async def send_welcome(message: types.Message):
    # await message.reply('🤖 Добро пожаловать\n\n Вас приветсвует помощник системы\n <b>Центра Ортодонтии</b>!',
    #                     parse_mode=types.ParseMode.HTML)
    # keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    # keyboard.add(types.KeyboardButton(text="Отправить номер телефона 📱", request_contact=True))
    # await message.answer('Для получения доступа отправьте свой контакт\n', reply_markup=keyboard)
    # await PatientState.contact.set()
    markup = types.ReplyKeyboardMarkup()
    markup.add(types.KeyboardButton('Открыть веб страницу',
                                    web_app=WebAppInfo(url='https://9fad-37-110-214-40.ngrok-free.app/webapp/home-page/')))
    await message.answer('Здравствуйте, попробуйте наш WEB APP', reply_markup=markup)


@dp.message_handler(content_types=types.ContentTypes.CONTACT, state=PatientState.contact)
async def search_patient_by_contact(message: types.Message, state: FSMContext):
    contact = message.contact.phone_number
    if not contact.startswith('+'):
        contact = f'+{contact}'

    patient = Patient.objects.filter(phone=contact)
    if patient:
        await message.answer('✅ Ваш аккаунт успешно прошёл идентификацию!', reply_markup=types.ReplyKeyboardRemove())
        patient.update(chat_id=message.chat.id)
    else:
        await message.answer('❌Ваш номер не был зарегистрирован в стоматологии "<b>Центр ортодонтии</b>"',
                             reply_markup=types.ReplyKeyboardRemove(), parse_mode=types.ParseMode.HTML)
    await state.finish()

__all__ = ['dp']
