from aiogram import types
from aiogram.dispatcher import FSMContext
import aiogram.utils.markdown as fmt
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, InputMedia
from aiogram.utils.callback_data import CallbackData

from settings.config import bot, dp
from settings.states import AccountState, HouseCreateState, HouseUpdateState, FlatCreateState, FlatUpdateState, \
    AnnouncementCreateState, AnnouncementUpdateState, NotaryCreateState, NotaryUpdateState
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
announcement_callback = CallbackData("Announcement", "page", "token")
announcement_delete_callback = CallbackData("Announcement_delete", 'id', "token")
announcement_update_callback = CallbackData("Announcement_update", 'id', "token")
announcement_add_favorite = CallbackData("Announcement_add_favorite", 'user_id', 'announ_id', "token")


def get_announcement_keyboard(page, token) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=2)
    announcement_list = request_api.announcement_list(token)
    user_id = request_api.my_user_id(token)
    announcement_id = announcement_list[page]['id']

    has_next_page = len(announcement_list) > page + 1

    if page != 0:
        keyboard.insert(InlineKeyboardButton(
                text="< Назад",
                callback_data=announcement_callback.new(page=page - 1, token=token)))

    if has_next_page:
        keyboard.insert(InlineKeyboardButton(
                text="Вперёд >",
                callback_data=announcement_callback.new(page=page + 1, token=token)))

    keyboard.row(InlineKeyboardButton('Редактировать',
                                      callback_data=announcement_update_callback.new(id=announcement_id, token=token)),
                 InlineKeyboardButton('Удалить',
                                      callback_data=announcement_delete_callback.new(id=announcement_id, token=token)))
    return keyboard


@dp.message_handler(lambda message: message.text == "Объявления", state="*")
async def process_announcement_command(msg: types.Message, state: FSMContext):
    await state.reset_state()
    if request_db.is_auth(msg.from_user.id):
        await bot.send_message(msg.chat.id, 'Объявления:', reply_markup=key_admin.buttons_announcement)
        token = request_db.get_token_user(msg.from_user.id)
        announcement_list = request_api.announcement_list(token)
        announcement_data = announcement_list[0]
        keyboard = get_announcement_keyboard(page=0, token=token)  # Page: 0
        text = fmt.text(
            fmt.text(fmt.hbold("Учредительные документы: "), announcement_data['founding_documents']),
            fmt.text(fmt.hbold("Дом: "), announcement_data['purpose']),
            fmt.text(fmt.hbold("Кол-во комнат: "), announcement_data['count_rooms']),
            fmt.text(fmt.hbold("Планировка: "), announcement_data['layout']),
            fmt.text(fmt.hbold("Жилое состояние: "), announcement_data['residential_condition']),
            fmt.text(fmt.hbold("Общая площадь: "), announcement_data['all_square']),
            fmt.text(fmt.hbold("Балкон: "), announcement_data['balcony']),
            fmt.text(fmt.hbold("Тип отопления: "), announcement_data['heating_type']),
            fmt.text(fmt.hbold("Коммисия агенту: "), announcement_data['commission_to_agent']),
            fmt.text(fmt.hbold("Способ связи: "), announcement_data['connection_type']),
            fmt.text(fmt.hbold("Описание: "), announcement_data['description']),
            fmt.text(fmt.hbold("Цена: "), announcement_data['price']),
            fmt.text(fmt.hbold("Варианты расчета: "), announcement_data['calculation_option']),
            fmt.text(fmt.hbold("Карта: "), announcement_data['maps']),
            fmt.text(fmt.hbold("Статус: "), announcement_data['pub_status']),
            fmt.text(fmt.hbold("Дом: "), announcement_data['house']),
            fmt.text(fmt.hbold("Владелец: "), announcement_data['user']),
            sep="\n"
        )
        await bot.send_message(msg.chat.id, text, parse_mode="HTML", reply_markup=keyboard)
    else:
        await bot.send_message(msg.chat.id,
                               'Команда не доступна, вы не авторизованы, сначала авторизуйтесь',
                               reply_markup=key_auth.button_auth)


@dp.callback_query_handler(announcement_callback.filter())
async def announcement_page_handler(query: CallbackQuery, callback_data: dict):
    page = int(callback_data.get("page"))
    token = callback_data.get("token")
    data_list = request_api.announcement_list(token)

    announcement_data = data_list[page]
    keyboard = get_announcement_keyboard(page, token)
    text = fmt.text(
        fmt.text(fmt.hbold("Учредительные документы: "), announcement_data['founding_documents']),
        fmt.text(fmt.hbold("Дом: "), announcement_data['purpose']),
        fmt.text(fmt.hbold("Кол-во комнат: "), announcement_data['count_rooms']),
        fmt.text(fmt.hbold("Планировка: "), announcement_data['layout']),
        fmt.text(fmt.hbold("Жилое состояние: "), announcement_data['residential_condition']),
        fmt.text(fmt.hbold("Общая площадь: "), announcement_data['all_square']),
        fmt.text(fmt.hbold("Балкон: "), announcement_data['balcony']),
        fmt.text(fmt.hbold("Тип отопления: "), announcement_data['heating_type']),
        fmt.text(fmt.hbold("Коммисия агенту: "), announcement_data['commission_to_agent']),
        fmt.text(fmt.hbold("Способ связи: "), announcement_data['connection_type']),
        fmt.text(fmt.hbold("Описание: "), announcement_data['description']),
        fmt.text(fmt.hbold("Цена: "), announcement_data['price']),
        fmt.text(fmt.hbold("Варианты расчета: "), announcement_data['calculation_option']),
        fmt.text(fmt.hbold("Карта: "), announcement_data['maps']),
        fmt.text(fmt.hbold("Статус: "), announcement_data['pub_status']),
        fmt.text(fmt.hbold("Дом: "), announcement_data['house']),
        fmt.text(fmt.hbold("Владелец: "), announcement_data['user']),
        sep="\n"
    )

    await query.message.edit_text(text, parse_mode="HTML", reply_markup=keyboard)


@dp.callback_query_handler(announcement_delete_callback.filter())
async def announcement_delete_handler(query: CallbackQuery, callback_data: dict):
    id = int(callback_data.get("id"))
    token = callback_data.get("token")
    delete_data = request_api.announcement_delete(token, id)

    if delete_data:
        text = 'Объявление успешно удалено! Нажмите "Объявления" для обновления актуальных данных'
    else:
        text = 'Усп, что-то пошло не так.'

    await query.message.answer(text, reply_markup=key_admin.button_announcement_cancel)


@dp.callback_query_handler(announcement_update_callback.filter())
async def announcement_update_handler(query: CallbackQuery, callback_data: dict, state: FSMContext):
    id = int(callback_data.get("id"))
    token = callback_data.get("token")
    announcement_data = request_api.announcement_detail(token, id)
    text = fmt.text(
        fmt.text(fmt.hbold("*** Скопируйте шаблон без этой строки ***")),
        fmt.text(fmt.hbold("Учредительные документы: "), announcement_data['founding_documents']),
        fmt.text(fmt.hbold("Дом: "), announcement_data['purpose']),
        fmt.text(fmt.hbold("Кол-во комнат: "), announcement_data['count_rooms']),
        fmt.text(fmt.hbold("Планировка: "), announcement_data['layout']),
        fmt.text(fmt.hbold("Жилое состояние: "), announcement_data['residential_condition']),
        fmt.text(fmt.hbold("Общая площадь: "), announcement_data['all_square']),
        fmt.text(fmt.hbold("Балкон: "), announcement_data['balcony']),
        fmt.text(fmt.hbold("Тип отопления: "), announcement_data['heating_type']),
        fmt.text(fmt.hbold("Коммисия агенту: "), announcement_data['commission_to_agent']),
        fmt.text(fmt.hbold("Способ связи: "), announcement_data['connection_type']),
        fmt.text(fmt.hbold("Описание: "), announcement_data['description']),
        fmt.text(fmt.hbold("Цена: "), announcement_data['price']),
        fmt.text(fmt.hbold("Варианты расчета: "), announcement_data['calculation_option']),
        fmt.text(fmt.hbold("Карта: "), announcement_data['maps']),
        fmt.text(fmt.hbold("Статус: "), announcement_data['pub_status']),
        fmt.text(fmt.hbold("Дом: "), announcement_data['house']),
        fmt.text(fmt.hbold("Владелец: "), announcement_data['user']),
        sep="\n"
    )
    await state.update_data(id=id)
    await AnnouncementUpdateState.save.set()
    await query.message.answer(text, parse_mode="HTML", reply_markup=key_admin.button_announcement_cancel)


@dp.message_handler(state=AnnouncementUpdateState.save)
async def announcement_update_state(msg: types.Message, state: FSMContext):
    announcement_data = msg.text
    data = await state.get_data()
    id = data.get('id')
    token = request_db.get_token_user(msg.from_user.id)
    announcement_data = announcement_data.split('\n')
    data_for_save = []
    for data in announcement_data:
        data = data.split(':')
        data_for_save.append(data[1].strip())

    save_data = request_api.announcement_update(token, id, data_for_save)
    if save_data:
        await bot.send_message(msg.chat.id, 'Объявление успешно обновлено.',
                               reply_markup=key_admin.button_announcement_cancel)
    else:
        await bot.send_message(msg.chat.id, 'Усп, что-то пошло не так.',
                               reply_markup=key_admin.button_announcement_cancel)
    await state.reset_state()


@dp.message_handler(lambda message: message.text == "Добавить объявление")
async def process_announcement_create_command(msg: types.Message, state: FSMContext):
    if request_db.is_auth(msg.from_user.id):
        token = request_db.get_token_user(msg.from_user.id)
        await bot.send_message(msg.chat.id, 'Скопируйте шаблон и подставте свои данные вместо ***',
                               reply_markup=key_admin.button_announcement_cancel)

        text = fmt.text(
            fmt.text(fmt.hbold("|Учредительные документы: "), "***"),
            fmt.text(fmt.hbold("|Дом: "), "***"),
            fmt.text(fmt.hbold("|Кол-во комнат: "), "***"),
            fmt.text(fmt.hbold("|Планировка: "), "***"),
            fmt.text(fmt.hbold("|Жилое состояние: "), "***"),
            fmt.text(fmt.hbold("|Общая площадь: "), "***"),
            fmt.text(fmt.hbold("|Балкон: "), "***"),
            fmt.text(fmt.hbold("|Тип отопления: "), "***"),
            fmt.text(fmt.hbold("|Коммисия агенту: "), "***"),
            fmt.text(fmt.hbold("|Способ связи: "), "***"),
            fmt.text(fmt.hbold("|Описание: "), "***"),
            fmt.text(fmt.hbold("|Цена: "), "***"),
            fmt.text(fmt.hbold("|Варианты расчета: "), "***"),
            fmt.text(fmt.hbold("|Карта: "), "***"),
            fmt.text(fmt.hbold("|Статус: "), "***"),
            fmt.text(fmt.hbold("|Дом: "), "***"),
            sep="\n"
        )
        await bot.send_message(msg.chat.id, text, parse_mode="HTML")
        await AnnouncementCreateState.save.set()
    else:
        await bot.send_message(msg.chat.id,
                               'Команда не доступна, вы не авторизованы, сначала авторизуйтесь',
                               reply_markup=key_auth.button_auth)


@dp.message_handler(state=AnnouncementCreateState.save)
async def announcement_create_state(msg: types.Message, state: FSMContext):
    announcement_data = msg.text
    await state.reset_state()
    token = request_db.get_token_user(msg.from_user.id)
    announcement_data = announcement_data.split('\n')
    data_for_save = []
    for data in announcement_data:
        data = data.split(':')
        data_for_save.append(data[1].strip())

    save_data = request_api.announcement_create(token, data_for_save)
    if save_data:
        await bot.send_message(msg.chat.id, 'Объявление успешно добавлено.',
                               reply_markup=key_admin.button_announcement_cancel)
    else:
        await bot.send_message(msg.chat.id, 'Усп, что-то пошло не так.',
                               reply_markup=key_admin.button_announcement_cancel)


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


@dp.callback_query_handler(house_update_callback.filter())
async def house_update_handler(query: CallbackQuery, callback_data: dict, state: FSMContext):
    id = int(callback_data.get("id"))
    token = callback_data.get("token")
    house_data = request_api.house_detail(token, id)
    text = fmt.text(
        fmt.text(fmt.hbold("*** Скопируйте шаблон (без этой строки) и произвидите изминения ***")),
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
        sep="\n"
    )
    await state.update_data(id=id)
    await HouseUpdateState.save.set()
    await query.message.answer(text, parse_mode="HTML", reply_markup=key_admin.button_house_cancel)


@dp.message_handler(state=HouseUpdateState.save)
async def house_update_state(msg: types.Message, state: FSMContext):
    house_data = msg.text
    data = await state.get_data()
    id = data.get('id')
    token = request_db.get_token_user(msg.from_user.id)
    house_data = house_data.split('\n')
    data_for_save = []
    for data in house_data:
        data = data.split(':')
        data_for_save.append(data[1].strip())

    save_data = request_api.house_update(token, id, data_for_save)
    if save_data:
        await bot.send_message(msg.chat.id, 'Дом успешно обновлен.',
                               reply_markup=key_admin.button_house_cancel)
    else:
        await bot.send_message(msg.chat.id, 'Усп, что-то пошло не так.',
                               reply_markup=key_admin.button_house_cancel)
    await state.reset_state()


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
async def house_create_state(msg: types.Message, state: FSMContext):
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
flat_callback = CallbackData("Flat", "page", "token")
flat_delete_callback = CallbackData("Flat_delete", 'id', "token")
flat_update_callback = CallbackData("Flat_update", 'id', "token")


def get_flat_keyboard(page, token) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=2)
    flat_list = request_api.flat_list(token)
    flat_id = flat_list[page]['id']
    has_next_page = len(flat_list) > page + 1
    if page != 0:
        keyboard.insert(InlineKeyboardButton(
                text="< Назад",
                callback_data=flat_callback.new(page=page - 1, token=token)))

    if has_next_page:
        keyboard.insert(InlineKeyboardButton(
                text="Вперёд >",
                callback_data=flat_callback.new(page=page + 1, token=token)))

    keyboard.row(InlineKeyboardButton('Редактировать',
                                      callback_data=flat_update_callback.new(id=flat_id, token=token)),
                 InlineKeyboardButton('Удалить',
                                      callback_data=flat_delete_callback.new(id=flat_id, token=token)))
    return keyboard


@dp.message_handler(lambda message: message.text == "Квартиры", state="*")
async def process_flat_command(msg: types.Message, state: FSMContext):
    await state.reset_state()
    if request_db.is_auth(msg.from_user.id):
        await bot.send_message(msg.chat.id, 'Квартиры:', reply_markup=key_admin.buttons_flat)
        token = request_db.get_token_user(msg.from_user.id)
        flat_list = request_api.flat_list(token)
        flat_data = flat_list[0]
        keyboard = get_flat_keyboard(page=0, token=token)  # Page: 0
        text = fmt.text(
            fmt.text(fmt.hbold("Дом: "), flat_data['house']),
            fmt.text(fmt.hbold("Корпус: "), flat_data['house_building']),
            fmt.text(fmt.hbold("Секция: "), flat_data['section']),
            fmt.text(fmt.hbold("Этаж: "), flat_data['floor']),
            fmt.text(fmt.hbold("Номер квартиры: "), flat_data['number']),
            fmt.text(fmt.hbold("Стояк: "), flat_data['riser']),
            fmt.text(fmt.hbold("Количесво комнат: "), flat_data['count_room']),
            fmt.text(fmt.hbold("Площадь: "), flat_data['square']),
            fmt.text(fmt.hbold("Цена за м.кв: "), flat_data['price_per_meter']),
            fmt.text(fmt.hbold("Забронирована: "), flat_data['reserved']),
            fmt.text(fmt.hbold("Создатель: "), flat_data['creator']),
            sep="\n"
        )
        await bot.send_message(msg.chat.id, text, parse_mode="HTML", reply_markup=keyboard)
    else:
        await bot.send_message(msg.chat.id,
                               'Команда не доступна, вы не авторизованы, сначала авторизуйтесь',
                               reply_markup=key_auth.button_auth)


@dp.callback_query_handler(flat_callback.filter())
async def flat_page_handler(query: CallbackQuery, callback_data: dict):
    page = int(callback_data.get("page"))
    token = callback_data.get("token")
    data_list = request_api.flat_list(token)

    flat_data = data_list[page]
    keyboard = get_flat_keyboard(page, token)
    text = fmt.text(
        fmt.text(fmt.hbold("Дом: "), flat_data['house']),
        fmt.text(fmt.hbold("Корпус: "), flat_data['house_building']),
        fmt.text(fmt.hbold("Секция: "), flat_data['section']),
        fmt.text(fmt.hbold("Этаж: "), flat_data['floor']),
        fmt.text(fmt.hbold("Номер квартиры: "), flat_data['number']),
        fmt.text(fmt.hbold("Стояк: "), flat_data['riser']),
        fmt.text(fmt.hbold("Количесво комнат: "), flat_data['count_room']),
        fmt.text(fmt.hbold("Площадь: "), flat_data['square']),
        fmt.text(fmt.hbold("Цена за м.кв: "), flat_data['price_per_meter']),
        fmt.text(fmt.hbold("Забронирована: "), flat_data['reserved']),
        fmt.text(fmt.hbold("Создатель: "), flat_data['creator']),
        sep="\n"
    )

    await query.message.edit_text(text, parse_mode="HTML", reply_markup=keyboard)


@dp.callback_query_handler(flat_delete_callback.filter())
async def flat_delete_handler(query: CallbackQuery, callback_data: dict):
    id = int(callback_data.get("id"))
    token = callback_data.get("token")
    delete_data = request_api.flat_delete(token, id)

    if delete_data:
        text = 'Квартира успешно удален! Нажмите "Квартиры" для обновления актуальных данных'
    else:
        text = 'Усп, что-то пошло не так.'

    await query.message.answer(text, reply_markup=key_admin.button_flat_cancel)


@dp.callback_query_handler(flat_update_callback.filter())
async def flat_update_handler(query: CallbackQuery, callback_data: dict, state: FSMContext):
    id = int(callback_data.get("id"))
    token = callback_data.get("token")
    flat_data = request_api.flat_detail(token, id)
    text = fmt.text(
        fmt.text(fmt.hbold("*** Скопируйте шаблон без этой строки ***")),
        fmt.text(fmt.hbold("Дом: "), flat_data['house']),
        fmt.text(fmt.hbold("Корпус: "), flat_data['house_building']),
        fmt.text(fmt.hbold("Секция: "), flat_data['section']),
        fmt.text(fmt.hbold("Этаж: "), flat_data['floor']),
        fmt.text(fmt.hbold("Номер квартиры: "), flat_data['number']),
        fmt.text(fmt.hbold("Стояк: "), flat_data['riser']),
        fmt.text(fmt.hbold("Количесво комнат: "), flat_data['count_room']),
        fmt.text(fmt.hbold("Площадь: "), flat_data['square']),
        fmt.text(fmt.hbold("Цена за м.кв: "), flat_data['price_per_meter']),
        fmt.text(fmt.hbold("Забронирована: "), flat_data['reserved']),
        fmt.text(fmt.hbold("Создатель: "), flat_data['creator']),
        sep="\n"
    )
    await state.update_data(id=id)
    await FlatUpdateState.save.set()
    await query.message.answer(text, parse_mode="HTML", reply_markup=key_admin.button_flat_cancel)


@dp.message_handler(state=FlatUpdateState.save)
async def flat_update_state(msg: types.Message, state: FSMContext):
    flat_data = msg.text
    data = await state.get_data()
    id = data.get('id')
    token = request_db.get_token_user(msg.from_user.id)
    flat_data = flat_data.split('\n')
    data_for_save = []
    for data in flat_data:
        data = data.split(':')
        data_for_save.append(data[1].strip())

    save_data = request_api.flat_update(token, id, data_for_save)
    if save_data:
        await bot.send_message(msg.chat.id, 'Квартира успешно обновлена.',
                               reply_markup=key_admin.button_flat_cancel)
    else:
        await bot.send_message(msg.chat.id, 'Усп, что-то пошло не так.',
                               reply_markup=key_admin.button_flat_cancel)
    await state.reset_state()


@dp.message_handler(lambda message: message.text == "Добавить квартиру")
async def process_flat_create_command(msg: types.Message, state: FSMContext):
    if request_db.is_auth(msg.from_user.id):
        token = request_db.get_token_user(msg.from_user.id)
        await bot.send_message(msg.chat.id, 'Скопируйте шаблон и подставте свои данные вместо ***',
                               reply_markup=key_admin.button_flat_cancel)
        text = fmt.text(
            fmt.text(fmt.hbold("|Дом: "), '***'),
            fmt.text(fmt.hbold("|Корпус: "), '***'),
            fmt.text(fmt.hbold("|Секция: "), '***'),
            fmt.text(fmt.hbold("|Этаж: "), '***'),
            fmt.text(fmt.hbold("|Номер квартиры: "), '***'),
            fmt.text(fmt.hbold("|Стояк: "), '***'),
            fmt.text(fmt.hbold("|Количесво комнат: "), '***'),
            fmt.text(fmt.hbold("|Площадь: "), '***'),
            fmt.text(fmt.hbold("|Цена за м.кв: "), '***'),
            fmt.text(fmt.hbold("|Забронирована: "), '***'),
            sep="\n"
        )
        await bot.send_message(msg.chat.id, text, parse_mode="HTML")
        await FlatCreateState.save.set()
    else:
        await bot.send_message(msg.chat.id,
                               'Команда не доступна, вы не авторизованы, сначала авторизуйтесь',
                               reply_markup=key_auth.button_auth)


@dp.message_handler(state=FlatCreateState.save)
async def flat_create_state(msg: types.Message, state: FSMContext):
    flat_data = msg.text
    await state.reset_state()
    token = request_db.get_token_user(msg.from_user.id)
    flat_data = flat_data.split('\n')
    data_for_save = []
    for data in flat_data:
        data = data.split(':')
        data_for_save.append(data[1].strip())

    save_data = request_api.flat_create(token, data_for_save)
    if save_data:
        await bot.send_message(msg.chat.id, 'Квартира успешно добавлена.',
                               reply_markup=key_admin.button_flat_cancel)
    else:
        await bot.send_message(msg.chat.id, 'Усп, что-то пошло не так.',
                               reply_markup=key_admin.button_flat_cancel)


# notary
notary_callback = CallbackData("Notary", "page", "token")
notary_delete_callback = CallbackData("Notary_delete", 'id', "token")
notary_update_callback = CallbackData("Notary_update", 'id', "token")


def get_notary_keyboard(page, token) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=2)
    notary_list = request_api.notary_list(token)
    notary_id = notary_list[page]['id']
    has_next_page = len(notary_list) > page + 1
    if page != 0:
        keyboard.insert(InlineKeyboardButton(
                text="< Назад",
                callback_data=notary_callback.new(page=page - 1, token=token)))

    if has_next_page:
        keyboard.insert(InlineKeyboardButton(
                text="Вперёд >",
                callback_data=notary_callback.new(page=page + 1, token=token)))

    keyboard.row(InlineKeyboardButton('Редактировать',
                                      callback_data=notary_update_callback.new(id=notary_id, token=token)),
                 InlineKeyboardButton('Удалить',
                                      callback_data=notary_delete_callback.new(id=notary_id, token=token)))
    return keyboard


@dp.message_handler(lambda message: message.text == "Нотариусы", state="*")
async def process_notary_command(msg: types.Message, state: FSMContext):
    await state.reset_state()
    if request_db.is_auth(msg.from_user.id):
        await bot.send_message(msg.chat.id, 'Нотариусы:', reply_markup=key_admin.buttons_notary)
        token = request_db.get_token_user(msg.from_user.id)
        notary_list = request_api.notary_list(token)
        notary_data = notary_list[0]
        keyboard = get_notary_keyboard(page=0, token=token)  # Page: 0
        text = fmt.text(
            fmt.text(fmt.hbold("Имя: "), notary_data['first_name']),
            fmt.text(fmt.hbold("Фамилия: "), notary_data['last_name']),
            fmt.text(fmt.hbold("Телефон: "), notary_data['phone']),
            fmt.text(fmt.hbold("Email: "), notary_data['email']),
            sep="\n"
        )
        await bot.send_message(msg.chat.id, text, parse_mode="HTML", reply_markup=keyboard)
    else:
        await bot.send_message(msg.chat.id,
                               'Команда не доступна, вы не авторизованы, сначала авторизуйтесь',
                               reply_markup=key_auth.button_auth)


@dp.callback_query_handler(notary_callback.filter())
async def notary_page_handler(query: CallbackQuery, callback_data: dict):
    page = int(callback_data.get("page"))
    token = callback_data.get("token")
    data_list = request_api.notary_list(token)

    notary_data = data_list[page]
    keyboard = get_notary_keyboard(page, token)
    text = fmt.text(
        fmt.text(fmt.hbold("Имя: "), notary_data['first_name']),
        fmt.text(fmt.hbold("Фамилия: "), notary_data['last_name']),
        fmt.text(fmt.hbold("Телефон: "), notary_data['phone']),
        fmt.text(fmt.hbold("Email: "), notary_data['email']),
        sep="\n"
    )

    await query.message.edit_text(text, parse_mode="HTML", reply_markup=keyboard)


@dp.callback_query_handler(notary_delete_callback.filter())
async def notary_delete_handler(query: CallbackQuery, callback_data: dict):
    id = int(callback_data.get("id"))
    token = callback_data.get("token")
    delete_data = request_api.notary_delete(token, id)

    if delete_data:
        text = 'Нотариус успешно удален! Нажмите "Нотариусы" для обновления актуальных данных'
    else:
        text = 'Усп, что-то пошло не так.'

    await query.message.answer(text, reply_markup=key_admin.button_notary_cancel)


@dp.callback_query_handler(notary_update_callback.filter())
async def notary_update_handler(query: CallbackQuery, callback_data: dict, state: FSMContext):
    id = int(callback_data.get("id"))
    token = callback_data.get("token")
    notary_data = request_api.notary_detail(token, id)
    text = fmt.text(
        fmt.text(fmt.hbold("*** Скопируйте шаблон без этой строки ***")),
        fmt.text(fmt.hbold("Имя: "), notary_data['first_name']),
        fmt.text(fmt.hbold("Фамилия: "), notary_data['last_name']),
        fmt.text(fmt.hbold("Телефон: "), notary_data['phone']),
        fmt.text(fmt.hbold("Email: "), notary_data['email']),
        sep="\n"
    )
    await state.update_data(id=id)
    await NotaryUpdateState.save.set()
    await query.message.answer(text, parse_mode="HTML", reply_markup=key_admin.button_notary_cancel)


@dp.message_handler(state=NotaryUpdateState.save)
async def notary_update_state(msg: types.Message, state: FSMContext):
    notary_data = msg.text
    data = await state.get_data()
    id = data.get('id')
    token = request_db.get_token_user(msg.from_user.id)
    notary_data = notary_data.split('\n')
    data_for_save = []
    for data in notary_data:
        data = data.split(':')
        data_for_save.append(data[1].strip())

    save_data = request_api.notary_update(token, id, data_for_save)
    if save_data:
        await bot.send_message(msg.chat.id, 'Данные успешно обновлены.',
                               reply_markup=key_admin.button_notary_cancel)
    else:
        await bot.send_message(msg.chat.id, 'Усп, что-то пошло не так.',
                               reply_markup=key_admin.button_notary_cancel)
    await state.reset_state()


@dp.message_handler(lambda message: message.text == "Добавить нотариуса")
async def process_notary_create_command(msg: types.Message, state: FSMContext):
    if request_db.is_auth(msg.from_user.id):
        token = request_db.get_token_user(msg.from_user.id)
        await bot.send_message(msg.chat.id, 'Скопируйте шаблон и подставте свои данные вместо ***',
                               reply_markup=key_admin.button_notary_cancel)

        text = fmt.text(
            fmt.text(fmt.hbold("|Имя: "), "***"),
            fmt.text(fmt.hbold("|Фамилия: "), "***"),
            fmt.text(fmt.hbold("|Телефон: "), "***"),
            fmt.text(fmt.hbold("|Email: "), "***"),
            sep="\n"
        )
        await bot.send_message(msg.chat.id, text, parse_mode="HTML")
        await NotaryCreateState.save.set()
    else:
        await bot.send_message(msg.chat.id,
                               'Команда не доступна, вы не авторизованы, сначала авторизуйтесь',
                               reply_markup=key_auth.button_auth)


@dp.message_handler(state=NotaryCreateState.save)
async def notary_create_state(msg: types.Message, state: FSMContext):
    notary_data = msg.text
    await state.reset_state()
    token = request_db.get_token_user(msg.from_user.id)
    notary_data = notary_data.split('\n')
    data_for_save = []
    for data in notary_data:
        data = data.split(':')
        data_for_save.append(data[1].strip())

    save_data = request_api.notary_create(token, data_for_save)
    if save_data:
        await bot.send_message(msg.chat.id, 'Нотариус успешно добавлен.',
                               reply_markup=key_admin.button_notary_cancel)
    else:
        await bot.send_message(msg.chat.id, 'Усп, что-то пошло не так.',
                               reply_markup=key_admin.button_notary_cancel)

# user
user_callback = CallbackData("User", "page", "token")
user_blacklist_callback = CallbackData("User_blacklist", 'id', "token")


def get_user_keyboard(page, token) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=2)
    user_list = request_api.user_list(token)
    user_id = user_list[page]['pk']
    has_next_page = len(user_list) > page + 1
    if page != 0:
        keyboard.insert(InlineKeyboardButton(
                text="< Назад",
                callback_data=user_callback.new(page=page - 1, token=token)))

    if has_next_page:
        keyboard.insert(InlineKeyboardButton(
                text="Вперёд >",
                callback_data=user_callback.new(page=page + 1, token=token)))

    keyboard.row(InlineKeyboardButton('Добавить/Убрать из ЧС',
                                      callback_data=user_blacklist_callback.new(id=user_id, token=token)))
    return keyboard


@dp.message_handler(lambda message: message.text == "Пользователи", state="*")
async def process_user_command(msg: types.Message, state: FSMContext):
    await state.reset_state()
    if request_db.is_auth(msg.from_user.id):
        await bot.send_message(msg.chat.id, 'Пользователи:', reply_markup=key_admin.buttons_user)
        token = request_db.get_token_user(msg.from_user.id)
        user_list = request_api.user_list(token)
        user_data = user_list[0]
        keyboard = get_user_keyboard(page=0, token=token)  # Page: 0
        text = fmt.text(
            fmt.text(fmt.hbold("Имя: "), user_data['first_name']),
            fmt.text(fmt.hbold("Фамилия: "), user_data['last_name']),
            fmt.text(fmt.hbold("Телефон: "), user_data['phone']),
            fmt.text(fmt.hbold("Email: "), user_data['email']),
            fmt.text(fmt.hbold("Роль: "), user_data['role']),
            fmt.text(fmt.hbold("Черный список: "), user_data['is_blacklist']),
            sep="\n"
        )
        await bot.send_message(msg.chat.id, text, parse_mode="HTML", reply_markup=keyboard)
    else:
        await bot.send_message(msg.chat.id,
                               'Команда не доступна, вы не авторизованы, сначала авторизуйтесь',
                               reply_markup=key_auth.button_auth)


@dp.callback_query_handler(user_callback.filter())
async def user_page_handler(query: CallbackQuery, callback_data: dict):
    page = int(callback_data.get("page"))
    token = callback_data.get("token")
    data_list = request_api.user_list(token)

    user_data = data_list[page]
    keyboard = get_user_keyboard(page, token)
    text = fmt.text(
        fmt.text(fmt.hbold("Имя: "), user_data['first_name']),
        fmt.text(fmt.hbold("Фамилия: "), user_data['last_name']),
        fmt.text(fmt.hbold("Телефон: "), user_data['phone']),
        fmt.text(fmt.hbold("Email: "), user_data['email']),
        fmt.text(fmt.hbold("Роль: "), user_data['role']),
        fmt.text(fmt.hbold("Черный список: "), user_data['is_blacklist']),
        sep="\n"
    )

    await query.message.edit_text(text, parse_mode="HTML", reply_markup=keyboard)


@dp.callback_query_handler(user_blacklist_callback.filter())
async def user_blacklist_handler(query: CallbackQuery, callback_data: dict):
    id = int(callback_data.get("id"))
    token = callback_data.get("token")
    blacklist_data = request_api.user_blacklist_update(token, id)

    if blacklist_data:
        text = 'Пользователь добавлен/убран из ЧС'
    else:
        text = 'Усп, что-то пошло не так.'

    await query.message.answer(text, reply_markup=key_admin.button_user_cancel)

# user_blacklist
blacklist_callback = CallbackData("Blacklist", "page", "token")


def get_blacklist_keyboard(page, token) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=2)
    user_list = request_api.user_blacklist(token)
    user_id = user_list[page]['pk']
    has_next_page = len(user_list) > page + 1
    if page != 0:
        keyboard.insert(InlineKeyboardButton(
                text="< Назад",
                callback_data=blacklist_callback.new(page=page - 1, token=token)))

    if has_next_page:
        keyboard.insert(InlineKeyboardButton(
                text="Вперёд >",
                callback_data=blacklist_callback.new(page=page + 1, token=token)))

    keyboard.row(InlineKeyboardButton('Убрать из ЧС',
                                      callback_data=user_blacklist_callback.new(id=user_id, token=token)))
    return keyboard


@dp.message_handler(lambda message: message.text == "Черный список", state="*")
async def process_user_command(msg: types.Message, state: FSMContext):
    await state.reset_state()
    if request_db.is_auth(msg.from_user.id):
        await bot.send_message(msg.chat.id, 'Черный список:', reply_markup=key_admin.button_user_cancel)
        token = request_db.get_token_user(msg.from_user.id)
        user_list = request_api.user_blacklist(token)
        user_data = user_list[0]
        keyboard = get_blacklist_keyboard(page=0, token=token)  # Page: 0
        text = fmt.text(
            fmt.text(fmt.hbold("Имя: "), user_data['first_name']),
            fmt.text(fmt.hbold("Фамилия: "), user_data['last_name']),
            fmt.text(fmt.hbold("Телефон: "), user_data['phone']),
            fmt.text(fmt.hbold("Email: "), user_data['email']),
            fmt.text(fmt.hbold("Роль: "), user_data['role']),
            fmt.text(fmt.hbold("Черный список: "), user_data['is_blacklist']),
            sep="\n"
        )
        await bot.send_message(msg.chat.id, text, parse_mode="HTML", reply_markup=keyboard)
    else:
        await bot.send_message(msg.chat.id,
                               'Команда не доступна, вы не авторизованы, сначала авторизуйтесь',
                               reply_markup=key_auth.button_auth)


@dp.callback_query_handler(blacklist_callback.filter())
async def blacklist_page_handler(query: CallbackQuery, callback_data: dict):
    page = int(callback_data.get("page"))
    token = callback_data.get("token")
    data_list = request_api.user_blacklist(token)

    user_data = data_list[page]
    keyboard = get_blacklist_keyboard(page, token)
    text = fmt.text(
        fmt.text(fmt.hbold("Имя: "), user_data['first_name']),
        fmt.text(fmt.hbold("Фамилия: "), user_data['last_name']),
        fmt.text(fmt.hbold("Телефон: "), user_data['phone']),
        fmt.text(fmt.hbold("Email: "), user_data['email']),
        fmt.text(fmt.hbold("Роль: "), user_data['role']),
        fmt.text(fmt.hbold("Черный список: "), user_data['is_blacklist']),
        sep="\n"
    )

    await query.message.edit_text(text, parse_mode="HTML", reply_markup=keyboard)


# favorite
@dp.message_handler(lambda message: message.text == "Избранное", state=None)
async def process_profile_command(msg: types.Message):
    if request_db.is_auth(msg.from_user.id):
        token = request_db.get_token_user(msg.from_user.id)
        await bot.send_message(msg.chat.id, 'Зашли в избранное', reply_markup=key_base.button_cancel)
    else:
        await bot.send_message(msg.chat.id,
                               'Команда не доступна, вы не авторизованы, сначала авторизуйтесь',
                               reply_markup=key_auth.button_auth)

