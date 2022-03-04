from aiogram import types
from aiogram.dispatcher import FSMContext
import aiogram.utils.markdown as fmt
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, InputMedia
from aiogram.utils.callback_data import CallbackData

from settings.config import bot, dp
from settings.states import AccountState, HouseCreateState
from all_requests import request_api, request_db

from keyboards import auth as key_auth
from keyboards import base as key_base
from keyboards import admin as key_admin


# account
@dp.message_handler(lambda message: message.text == "Профиль", state="*")
async def process_profile_command(msg: types.Message, state: FSMContext):
    await state.reset_state()
    if request_db.is_auth(msg.from_user.id):
        token = request_db.get_token_user(msg.from_user.id)
        data = request_api.account_detail(token)
        text = fmt.text(
                    fmt.text(fmt.hbold("Имя пользователя: "), data['username']),
                    fmt.text(fmt.hbold("Email: "), data['email']),
                    fmt.text(fmt.hbold("Телефон: "), data['phone']),
                    fmt.text(fmt.hbold("Имя: "), data['first_name']),
                    fmt.text(fmt.hbold("Фамилия: "), data['last_name']),
                    fmt.text(fmt.hbold("Роль: "), data['role']),
                    sep="\n"
            )
        await bot.send_message(msg.chat.id, text, parse_mode="HTML", reply_markup=key_admin.buttons_account)
        await AccountState.switch.set()
    else:
        await bot.send_message(msg.chat.id,
                               'Команда не доступна, вы не авторизованы, сначала авторизуйтесь',
                               reply_markup=key_auth.button_auth)


@dp.message_handler(state=AccountState.switch)
async def account_switch(msg: types.Message, state: FSMContext):
    choice = msg.text
    if choice == 'Изменить номер телефона':
        await bot.send_message(msg.chat.id, 'Введите новый номер телефона', reply_markup=key_admin.button_account_cancel)
        await AccountState.phone.set()
    elif choice == 'Изменить имя':
        await bot.send_message(msg.chat.id, 'Введите имя', reply_markup=key_admin.button_account_cancel)
        await AccountState.first_name.set()
    elif choice == 'Изменить фамилию':
        await bot.send_message(msg.chat.id, 'Введите фамилию', reply_markup=key_admin.button_account_cancel)
        await AccountState.last_name.set()
    else:
        await bot.send_message(msg.chat.id, 'Я не знаю такой команды, попробуйте еще раз!')
        await AccountState.switch.set()


@dp.message_handler(state=AccountState.phone)
async def account_phone(msg: types.Message, state: FSMContext):
    phone = msg.text
    token = request_db.get_token_user(msg.from_user.id)
    save_data = request_api.account_update(token, phone=phone)
    await state.reset_state()
    if save_data:
        await bot.send_message(msg.chat.id, 'Новый номер указан.',
                               reply_markup=key_admin.button_account_cancel)
    else:
        await bot.send_message(msg.chat.id, 'Усп, что-то пошло не так.',
                               reply_markup=key_admin.button_account_cancel)


@dp.message_handler(state=AccountState.first_name)
async def account_first_name(msg: types.Message, state: FSMContext):
    first_name = msg.text
    token = request_db.get_token_user(msg.from_user.id)
    save_data = request_api.account_update(token, first_name=first_name)
    await state.reset_state()
    if save_data:
        await bot.send_message(msg.chat.id, 'Новое имя указано.',
                               reply_markup=key_admin.button_account_cancel)
    else:
        await bot.send_message(msg.chat.id, 'Усп, что-то пошло не так.',
                               reply_markup=key_admin.button_account_cancel)


@dp.message_handler(state=AccountState.last_name)
async def account_last_name(msg: types.Message, state: FSMContext):
    last_name = msg.text
    token = request_db.get_token_user(msg.from_user.id)
    save_data = request_api.account_update(token, last_name=last_name)
    await state.reset_state()
    if save_data:
        await bot.send_message(msg.chat.id, 'Новая фамилия указана.',
                               reply_markup=key_admin.button_account_cancel)
    else:
        await bot.send_message(msg.chat.id, 'Усп, что-то пошло не так.',
                               reply_markup=key_admin.button_account_cancel)


# announcement
@dp.message_handler(lambda message: message.text == "Объявления", state=None)
async def process_announcement_command(msg: types.Message):
    if request_db.is_auth(msg.from_user.id):
        token = request_db.get_token_user(msg.from_user.id)
        await bot.send_message(msg.chat.id, 'Зашли в Объявления', reply_markup=key_base.button_cancel)
    else:
        await bot.send_message(msg.chat.id,
                               'Команда не доступна, вы не авторизованы, сначала авторизуйтесь',
                               reply_markup=key_auth.button_auth)


# house
houses_callback = CallbackData("Houses", "page", "token")
house_delete_callback = CallbackData("House_delete", 'id', "token")
house_update_callback = CallbackData("House_update", 'id', "token")


def get_houses_keyboard(page, token) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=2)
    house_list = request_api.house_list(token)
    house_id = house_list[page]['id']
    has_next_page = len(house_list) > page + 1
    if page != 0:
        keyboard.insert(InlineKeyboardButton(
                text="< Назад",
                callback_data=houses_callback.new(page=page - 1, token=token)))

    if has_next_page:
        keyboard.insert(InlineKeyboardButton(
                text="Вперёд >",
                callback_data=houses_callback.new(page=page + 1, token=token)))

    keyboard.row(InlineKeyboardButton('Редактировать',
                                      callback_data=house_update_callback.new(id=house_id, token=token)),
                 InlineKeyboardButton('Удалить',
                                      callback_data=house_delete_callback.new(id=house_id, token=token)))
    return keyboard


@dp.message_handler(lambda message: message.text == "Дома", state="*")
async def process_house_command(msg: types.Message, state: FSMContext):
    await state.reset_state()
    if request_db.is_auth(msg.from_user.id):
        await bot.send_message(msg.chat.id, 'Дома:', reply_markup=key_admin.buttons_house)
        token = request_db.get_token_user(msg.from_user.id)
        house_list = request_api.house_list(token)
        house_data = house_list[0]
        keyboard = get_houses_keyboard(page=0, token=token)  # Page: 0
        text = fmt.text(
            fmt.text(fmt.hbold("Название дома: "), house_data['name']),
            fmt.text(fmt.hbold("Район: "), house_data['district']),
            fmt.text(fmt.hbold("Микрорайон: "), house_data['microdistrict']),
            fmt.text(fmt.hbold("Улица: "), house_data['street']),
            fmt.text(fmt.hbold("Номер: "), house_data['number']),
            fmt.text(fmt.hbold("Описание: "), house_data['description']),
            fmt.text(fmt.hbold("Статус ЖК: "), house_data['lcd_status']),
            fmt.text(fmt.hbold("Тип дома: "), house_data['type_house']),
            fmt.text(fmt.hbold("Класс дома: "), house_data['class_house']),
            fmt.text(fmt.hbold("Технологии: "), house_data['technologies']),
            fmt.text(fmt.hbold("Расстояние до моря: "), house_data['to_sea']),
            fmt.text(fmt.hbold("Коммунальные платежы: "), house_data['payments']),
            fmt.text(fmt.hbold("Высота потолка: "), house_data['ceiling_height']),
            fmt.text(fmt.hbold("Газ: "), house_data['gas']),
            fmt.text(fmt.hbold("Отопление: "), house_data['heating']),
            fmt.text(fmt.hbold("Канализация: "), house_data['sewerage']),
            fmt.text(fmt.hbold("Менеджер по продажам: "), house_data['sales_dep_fullname']),
            fmt.text(fmt.hbold("Телефон менеджера: "), house_data['sales_dep_phone']),
            fmt.text(fmt.hbold("Email менеджера: "), house_data['sales_dep_email']),
            fmt.text(fmt.hbold("Оформление: "), house_data['registration']),
            fmt.text(fmt.hbold("Варианты расчета: "), house_data['calculation_options']),
            fmt.text(fmt.hbold("Назначение: "), house_data['appointment']),
            fmt.text(fmt.hbold("Сумма в договоре : "), house_data['sum_in_contract']),
            fmt.text(fmt.hbold("Статус: "), house_data['state']),
            fmt.text(fmt.hbold("Территория: "), house_data['territory']),
            fmt.text(fmt.hbold("Карта: "), house_data['maps']),
            fmt.text(fmt.hbold("Кол-во корпусов: "), house_data['house_buildings']),
            fmt.text(fmt.hbold("Кол-во секций: "), house_data['sections']),
            fmt.text(fmt.hbold("Кол-во этажей: "), house_data['floors']),
            fmt.text(fmt.hbold("Кол-во стояков: "), house_data['risers']),
            fmt.text(fmt.hbold("Строитель: "), house_data['builder']),
            sep="\n"
        )
        await bot.send_message(msg.chat.id, text, parse_mode="HTML", reply_markup=keyboard)
    else:
        await bot.send_message(msg.chat.id,
                               'Команда не доступна, вы не авторизованы, сначала авторизуйтесь',
                               reply_markup=key_auth.button_auth)


@dp.callback_query_handler(houses_callback.filter())
async def house_page_handler(query: CallbackQuery, callback_data: dict):
    page = int(callback_data.get("page"))
    token = callback_data.get("token")
    data_list = request_api.house_list(token)

    house_data = data_list[page]
    keyboard = get_houses_keyboard(page, token)
    text = fmt.text(
        fmt.text(fmt.hbold("Название дома: "), house_data['name']),
        fmt.text(fmt.hbold("Район: "), house_data['district']),
        fmt.text(fmt.hbold("Микрорайон: "), house_data['microdistrict']),
        fmt.text(fmt.hbold("Улица: "), house_data['street']),
        fmt.text(fmt.hbold("Номер: "), house_data['number']),
        fmt.text(fmt.hbold("Описание: "), house_data['description']),
        fmt.text(fmt.hbold("Статус ЖК: "), house_data['lcd_status']),
        fmt.text(fmt.hbold("Тип дома: "), house_data['type_house']),
        fmt.text(fmt.hbold("Класс дома: "), house_data['class_house']),
        fmt.text(fmt.hbold("Технологии: "), house_data['technologies']),
        fmt.text(fmt.hbold("Расстояние до моря: "), house_data['to_sea']),
        fmt.text(fmt.hbold("Коммунальные платежы: "), house_data['payments']),
        fmt.text(fmt.hbold("Высота потолка: "), house_data['ceiling_height']),
        fmt.text(fmt.hbold("Газ: "), house_data['gas']),
        fmt.text(fmt.hbold("Отопление: "), house_data['heating']),
        fmt.text(fmt.hbold("Канализация: "), house_data['sewerage']),
        fmt.text(fmt.hbold("Менеджер по продажам: "), house_data['sales_dep_fullname']),
        fmt.text(fmt.hbold("Телефон менеджера: "), house_data['sales_dep_phone']),
        fmt.text(fmt.hbold("Email менеджера: "), house_data['sales_dep_email']),
        fmt.text(fmt.hbold("Оформление: "), house_data['registration']),
        fmt.text(fmt.hbold("Варианты расчета: "), house_data['calculation_options']),
        fmt.text(fmt.hbold("Назначение: "), house_data['appointment']),
        fmt.text(fmt.hbold("Сумма в договоре : "), house_data['sum_in_contract']),
        fmt.text(fmt.hbold("Статус: "), house_data['state']),
        fmt.text(fmt.hbold("Территория: "), house_data['territory']),
        fmt.text(fmt.hbold("Карта: "), house_data['maps']),
        fmt.text(fmt.hbold("Кол-во корпусов: "), house_data['house_buildings']),
        fmt.text(fmt.hbold("Кол-во секций: "), house_data['sections']),
        fmt.text(fmt.hbold("Кол-во этажей: "), house_data['floors']),
        fmt.text(fmt.hbold("Кол-во стояков: "), house_data['risers']),
        fmt.text(fmt.hbold("Строитель: "), house_data['builder']),
        sep="\n"
    )

    await query.message.edit_text(text, parse_mode="HTML", reply_markup=keyboard)


@dp.callback_query_handler(house_delete_callback.filter())
async def house_delete_handler(query: CallbackQuery, callback_data: dict):
    id = int(callback_data.get("id"))
    token = callback_data.get("token")
    delete_data = request_api.house_delete(token, id)

    if delete_data:
        text = 'Дом успешно удален! Нажмите "Дома" для обновления актуальных данных'
    else:
        text = 'Усп, что-то пошло не так.'

    await query.message.answer(text, reply_markup=key_admin.button_house_cancel)


@dp.message_handler(lambda message: message.text == "Добавить дом")
async def process_house_create_command(msg: types.Message, state: FSMContext):
    if request_db.is_auth(msg.from_user.id):
        token = request_db.get_token_user(msg.from_user.id)
        await bot.send_message(msg.chat.id, 'Скопируйте шаблон и подставте свои данные вместо ***',
                               reply_markup=key_admin.button_house_cancel)
        text = fmt.text(
            fmt.text(fmt.hbold("|Название дома: "), '***'),
            fmt.text(fmt.hbold("|Район: "), '***'),
            fmt.text(fmt.hbold("|Микрорайон: "), '***'),
            fmt.text(fmt.hbold("|Улица: "), '***'),
            fmt.text(fmt.hbold("|Номер: "), '***'),
            fmt.text(fmt.hbold("|Описание: "), '***'),
            fmt.text(fmt.hbold("|Статус ЖК: "), '***'),
            fmt.text(fmt.hbold("|Тип дома: "), '***'),
            fmt.text(fmt.hbold("|Класс дома: "), '***'),
            fmt.text(fmt.hbold("|Технологии: "), '***'),
            fmt.text(fmt.hbold("|Расстояние до моря: "), '***'),
            fmt.text(fmt.hbold("|Коммунальные платежы: "), '***'),
            fmt.text(fmt.hbold("|Высота потолка: "), '***'),
            fmt.text(fmt.hbold("|Газ: "), '***'),
            fmt.text(fmt.hbold("|Отопление: "), '***'),
            fmt.text(fmt.hbold("|Канализация: "), '***'),
            fmt.text(fmt.hbold("|Менеджер по продажам: "), '***'),
            fmt.text(fmt.hbold("|Телефон менеджера: "), '***'),
            fmt.text(fmt.hbold("|Email менеджера: "), '***'),
            fmt.text(fmt.hbold("|Оформление: "), '***'),
            fmt.text(fmt.hbold("|Варианты расчета: "), '***'),
            fmt.text(fmt.hbold("|Назначение: "), '***'),
            fmt.text(fmt.hbold("|Сумма в договоре : "), '***'),
            fmt.text(fmt.hbold("|Статус: "), '***'),
            fmt.text(fmt.hbold("|Территория: "), '***'),
            fmt.text(fmt.hbold("|Карта: "), '***'),
            fmt.text(fmt.hbold("|Кол-во корпусов: "), '***'),
            fmt.text(fmt.hbold("|Кол-во секций: "), '***'),
            fmt.text(fmt.hbold("|Кол-во этажей: "), '***'),
            fmt.text(fmt.hbold("|Кол-во стояков: "), '***'),
            sep="\n"
        )
        await bot.send_message(msg.chat.id, text, parse_mode="HTML")
        await HouseCreateState.save.set()
    else:
        await bot.send_message(msg.chat.id,
                               'Команда не доступна, вы не авторизованы, сначала авторизуйтесь',
                               reply_markup=key_auth.button_auth)


@dp.message_handler(state=HouseCreateState.save)
async def account_last_name(msg: types.Message, state: FSMContext):
    house_data = msg.text
    await state.reset_state()
    token = request_db.get_token_user(msg.from_user.id)
    house_data = house_data.split('\n')
    data_for_save = []
    for data in house_data:
        data = data.split(':')
        data_for_save.append(data[1].strip())

    save_data = request_api.house_create(token, data_for_save)
    if save_data:
        await bot.send_message(msg.chat.id, 'Новай дом успешно добавлен.',
                               reply_markup=key_admin.button_house_cancel)
    else:
        await bot.send_message(msg.chat.id, 'Усп, что-то пошло не так.',
                               reply_markup=key_admin.button_house_cancel)


# flat
@dp.message_handler(lambda message: message.text == "Квартиры", state=None)
async def process_profile_command(msg: types.Message):
    if request_db.is_auth(msg.from_user.id):
        token = request_db.get_token_user(msg.from_user.id)
        await bot.send_message(msg.chat.id, 'Зашли в Квартиры', reply_markup=key_base.button_cancel)
    else:
        await bot.send_message(msg.chat.id,
                               'Команда не доступна, вы не авторизованы, сначала авторизуйтесь',
                               reply_markup=key_auth.button_auth)


@dp.message_handler(lambda message: message.text == "Нотариусы", state=None)
async def process_profile_command(msg: types.Message):
    if request_db.is_auth(msg.from_user.id):
        token = request_db.get_token_user(msg.from_user.id)
        await bot.send_message(msg.chat.id, 'Зашли в Нотариусы', reply_markup=key_base.button_cancel)
    else:
        await bot.send_message(msg.chat.id,
                               'Команда не доступна, вы не авторизованы, сначала авторизуйтесь',
                               reply_markup=key_auth.button_auth)


@dp.message_handler(lambda message: message.text == "Пользователи", state=None)
async def process_profile_command(msg: types.Message):
    if request_db.is_auth(msg.from_user.id):
        token = request_db.get_token_user(msg.from_user.id)
        await bot.send_message(msg.chat.id, 'Зашли в пользователей', reply_markup=key_base.button_cancel)
    else:
        await bot.send_message(msg.chat.id,
                               'Команда не доступна, вы не авторизованы, сначала авторизуйтесь',
                               reply_markup=key_auth.button_auth)


@dp.message_handler(lambda message: message.text == "Избранное", state=None)
async def process_profile_command(msg: types.Message):
    if request_db.is_auth(msg.from_user.id):
        token = request_db.get_token_user(msg.from_user.id)
        await bot.send_message(msg.chat.id, 'Зашли в избранное', reply_markup=key_base.button_cancel)
    else:
        await bot.send_message(msg.chat.id,
                               'Команда не доступна, вы не авторизованы, сначала авторизуйтесь',
                               reply_markup=key_auth.button_auth)

