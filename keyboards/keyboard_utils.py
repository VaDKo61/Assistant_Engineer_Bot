from typing import Dict

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

menu = [
    [
        InlineKeyboardButton(text='🛒 Купить', callback_data="generate_text"),
        InlineKeyboardButton(text='💲 Продать', callback_data="generate_text")
    ],
    [
        InlineKeyboardButton(text='Полезная информация', callback_data="generate_text")
    ]
]
menu = InlineKeyboardMarkup(inline_keyboard=menu)

