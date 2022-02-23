from aiogram.dispatcher.filters.state import State, StatesGroup


class LoginState(StatesGroup):
    email = State()
    password = State()


class RegistrationStates(StatesGroup):
    username = State()
    email = State()
    password = State()
    repeat_password = State()
    phone = State()

