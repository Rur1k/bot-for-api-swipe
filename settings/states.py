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
    wait_reg = State()
    edit_regdata = State()


class AccountState(StatesGroup):
    switch = State()
    phone = State()
    first_name = State()
    last_name = State()


class HouseCreateState(StatesGroup):
    save = State()


class HouseUpdateState(StatesGroup):
    save = State()


class FlatCreateState(StatesGroup):
    save = State()


class FlatUpdateState(StatesGroup):
    save = State()


class AnnouncementCreateState(StatesGroup):
    save = State()


class AnnouncementUpdateState(StatesGroup):
    save = State()


class NotaryCreateState(StatesGroup):
    save = State()


class NotaryUpdateState(StatesGroup):
    save = State()

