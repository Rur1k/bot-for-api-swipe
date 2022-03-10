from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

from .base import btn_cancel

btn_login = KeyboardButton('Вход')
btn_logout = KeyboardButton('Выход')
btn_registration = KeyboardButton('Регистрация')

btn_edit_regdata = KeyboardButton('Изменить данные')

button_auth = ReplyKeyboardMarkup(resize_keyboard=True).row(btn_login, btn_registration)

button_logout = ReplyKeyboardMarkup(resize_keyboard=True).add(btn_logout)

button_edit_regdata = ReplyKeyboardMarkup(resize_keyboard=True).row(btn_edit_regdata, btn_cancel)
