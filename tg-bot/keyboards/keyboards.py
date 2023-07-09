from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def get_main_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton('Прорахувати ціну')],
        [KeyboardButton('Перейти на сайт')],
        [KeyboardButton('Про проєкт')],
    ], resize_keyboard=True)
    return kb


def get_exit_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton('Назад 🔙')]
    ], resize_keyboard=True)
    return kb