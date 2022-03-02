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





