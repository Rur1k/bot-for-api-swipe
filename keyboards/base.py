from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton


btn_cancel = KeyboardButton('Отмена/Назад')

button_cancel = ReplyKeyboardMarkup(resize_keyboard=True).add(btn_cancel)
