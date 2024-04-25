from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from sqlalchemy.ext.asyncio import AsyncSession

from database.orm_query import orm_get_engineers


class ObjectCallbackFactory(CallbackData, prefix='object'):
    id: int


async def inline_kb_choose_engineer(session: AsyncSession):
    kb_builder = InlineKeyboardBuilder()
    buttons: list[InlineKeyboardButton] = []
    for engineer in await orm_get_engineers(session):
        buttons.append(InlineKeyboardButton(text=f'{engineer.firstname} {engineer.surname}',
                                            callback_data=ObjectCallbackFactory(id=engineer.id).pack()))
    kb_builder.row(*buttons, width=1)
    return kb_builder.as_markup()
