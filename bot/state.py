from aiogram.dispatcher.filters.state import StatesGroup, State


class PatientState(StatesGroup):
    contact = State()
