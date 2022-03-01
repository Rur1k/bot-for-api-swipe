from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

btn_login = KeyboardButton('Вход')
btn_logout = KeyboardButton('Выход')
btn_registration = KeyboardButton('Регистрация')

button_auth = ReplyKeyboardMarkup(resize_keyboard=True).row(btn_login, btn_registration)

button_logout = ReplyKeyboardMarkup(resize_keyboard=True).add(btn_logout)
