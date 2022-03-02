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


class AccountState(StatesGroup):
    switch = State()
    phone = State()
    first_name = State()
    last_name = State()

