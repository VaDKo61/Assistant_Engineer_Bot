from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from lexicon import replica


class EngineerCallbackFactory(CallbackData, prefix='engineer'):
    id: int
    action: str


async def inline_kb_engineer(engineer):
    text_answer = f'{engineer.firstname} {engineer.surname}'
    kb_builder = InlineKeyboardBuilder()
    buttons: list[InlineKeyboardButton] = []
    buttons.append(InlineKeyboardButton(text=replica.navigation['data'],
                                        callback_data=EngineerCallbackFactory(id=engineer.id, action='get').pack()))
    buttons.append(InlineKeyboardButton(text=replica.navigation['delete'],
                                        callback_data=EngineerCallbackFactory(id=engineer.id, action='del').pack()))
    kb_builder.row(*buttons, width=2)
    return text_answer, kb_builder.as_markup()
