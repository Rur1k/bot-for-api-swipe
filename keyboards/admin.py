from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
from .auth import btn_logout

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


