from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
from .auth import btn_logout
from .base import btn_cancel

# main menu
btn_account = KeyboardButton('Профиль')
btn_announcement = KeyboardButton('Объявления')
btn_house = KeyboardButton('Дома')
btn_flat = KeyboardButton('Квартиры')
btn_notary = KeyboardButton('Нотариусы')
btn_users = KeyboardButton('Пользователи')
btn_favorite = KeyboardButton('Избранное')


buttons_menu = ReplyKeyboardMarkup(resize_keyboard=True)
buttons_menu.row(btn_account, btn_announcement)
buttons_menu.row(btn_house, btn_flat)
buttons_menu.row(btn_notary, btn_users)
buttons_menu.row(btn_favorite, btn_logout)

# account
btn_set_phone = KeyboardButton('Изменить номер телефона')
btn_set_firstname = KeyboardButton('Изменить имя')
btn_set_lastname = KeyboardButton('Изменить фамилию')

buttons_account = ReplyKeyboardMarkup(resize_keyboard=True)
buttons_account.row(btn_set_phone, btn_set_firstname)
buttons_account.row(btn_set_lastname, btn_cancel)

button_account_cancel = ReplyKeyboardMarkup(resize_keyboard=True).add(btn_account)


# house
btn_house_create = KeyboardButton('Добавить дом')

buttons_house = ReplyKeyboardMarkup(resize_keyboard=True)
buttons_house.row(btn_house_create, btn_cancel)

button_house_cancel = ReplyKeyboardMarkup(resize_keyboard=True).add(btn_house)

# flat
btn_flat_create = KeyboardButton('Добавить квартиру')

buttons_flat = ReplyKeyboardMarkup(resize_keyboard=True)
buttons_flat.row(btn_flat_create, btn_cancel)

button_flat_cancel = ReplyKeyboardMarkup(resize_keyboard=True).add(btn_flat)

# annoucement
btn_announcement_create = KeyboardButton('Добавить объявление')

buttons_announcement = ReplyKeyboardMarkup(resize_keyboard=True)
buttons_announcement.row(btn_announcement_create, btn_cancel)

button_announcement_cancel = ReplyKeyboardMarkup(resize_keyboard=True).add(btn_announcement)

# notary
btn_notary_create = KeyboardButton('Добавить нотариуса')

buttons_notary = ReplyKeyboardMarkup(resize_keyboard=True)
buttons_notary.row(btn_notary_create, btn_cancel)

button_notary_cancel = ReplyKeyboardMarkup(resize_keyboard=True).add(btn_notary)

# user
btn_user_blacklist = KeyboardButton('Черный список')

buttons_user = ReplyKeyboardMarkup(resize_keyboard=True)
buttons_user.row(btn_user_blacklist, btn_cancel)

button_user_cancel = ReplyKeyboardMarkup(resize_keyboard=True).add(btn_users)



