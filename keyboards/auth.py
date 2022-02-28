from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

btn_login = KeyboardButton('Вход')
btn_registration = KeyboardButton('Регистрация')

button_auth = ReplyKeyboardMarkup(resize_keyboard=True)
button_auth.add(btn_login).add(btn_registration)

# inline_btn_login = InlineKeyboardButton('Вход', login')
# inline_btn_registration = InlineKeyboardButton('Регистрация', 'registration')
#
# inline_button_auth = InlineKeyboardMarkup(resize_keyboard=True)
# inline_button_auth.add(inline_btn_login).add(inline_btn_registration)
