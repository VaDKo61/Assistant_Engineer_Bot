from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import Object, Block
from database.orm_query import orm_get_engineers


class ObjectCallbackFactory(CallbackData, prefix='object'):
    id: int


class BlockCheckCallbackFactory(CallbackData, prefix='block_check'):
    id: int
    name: str
    object_id: int


class BlockLookCallbackFactory(CallbackData, prefix='block_look'):
    id: int


async def inline_kb_choose_engineer(session: AsyncSession):
    kb_builder = InlineKeyboardBuilder()
    buttons: list[InlineKeyboardButton] = []
    for engineer in await orm_get_engineers(session):
        buttons.append(InlineKeyboardButton(text=f'{engineer.firstname} {engineer.surname}',
                                            callback_data=ObjectCallbackFactory(id=engineer.id).pack()))
    kb_builder.row(*buttons, width=1)
    return kb_builder.as_markup()


async def inline_kb_object_block(block: Block, object_id: int):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(
        text='📑 Проверить узел',
        callback_data=BlockCheckCallbackFactory(id=block.id, name=block.name, object_id=object_id).pack())]])
    return keyboard


async def inline_kb_look_block(obj: Object):
    kb_builder = InlineKeyboardBuilder()
    buttons: list[InlineKeyboardButton] = []
    buttons.append(InlineKeyboardButton(text='📜 Показать узлы',
                                        callback_data=BlockLookCallbackFactory(id=obj.id).pack()))
    buttons.append(InlineKeyboardButton(text='➕ Добавить узел',
                                        callback_data=f'add_block.{obj.id}'))
    kb_builder.row(*buttons, width=1)
    return kb_builder.as_markup()
