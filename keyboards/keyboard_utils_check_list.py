from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


async def inline_kb_check(stage: str):
    kb_builder = InlineKeyboardBuilder()
    buttons: list[InlineKeyboardButton] = []
    buttons.append(InlineKeyboardButton(text='✅ Да', callback_data=stage))
    buttons.append(InlineKeyboardButton(text='❌ Нет', callback_data='check_cancel'))
    kb_builder.row(*buttons, width=2)
    return kb_builder.as_markup()
