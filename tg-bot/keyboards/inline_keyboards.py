from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def ikb_floor() -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton('Перший поверх', callback_data='First')],
        [InlineKeyboardButton('Останній поверх', callback_data='Last')],
        [InlineKeyboardButton('Не перший & не останній поверх', callback_data='Middle')]
    ])
    return ikb


def ikb_rooms() -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='1 кімната', callback_data='1')],
        [InlineKeyboardButton('2 кімнати', callback_data='2')],
        [InlineKeyboardButton('3 кімнати', callback_data='3')],
        [InlineKeyboardButton('4 кімнати', callback_data='4')],
        [InlineKeyboardButton('5+ кімнат', callback_data='5')]
    ])
    return ikb
