from aiogram import Router, F
from aiogram.enums import ContentType
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import CallbackQuery, Message
from sqlalchemy.ext.asyncio import AsyncSession

from database.orm_query import orm_add_block, orm_get_blocks_object
from keyboards.keyboard_utils_object_block import inline_kb_choose_engineer, ObjectCallbackFactory, \
    BlockLookCallbackFactory, \
    inline_kb_object_block
from states.states import FSMFillBlock

router_block = Router()


@router_block.callback_query(F.data.startswith('add_block'), StateFilter(default_state))
async def process_add_block_command(callback: CallbackQuery, state: FSMContext):
    await state.update_data(object_id=callback.data.split('.')[-1])
    await callback.message.answer('Введите имя узла:')
    await state.set_state(FSMFillBlock.name)


@router_block.message(StateFilter(FSMFillBlock.name), F.content_type == ContentType.TEXT)
async def process_name_sent(message: Message, state: FSMContext, session: AsyncSession):
    await state.update_data(name=message.text)
    await message.answer(text='Выберите ответственного за узел:',
                         reply_markup=await inline_kb_choose_engineer(session))
    await state.set_state(FSMFillBlock.engineer)


@router_block.message(StateFilter(FSMFillBlock.name))
async def warning_not_name(message: Message):
    await message.answer('Вы ввели некорректное имя узла!\nВведите имя узла.\nОтменить внесение данных - /cancel')


@router_block.callback_query(ObjectCallbackFactory.filter(), StateFilter(FSMFillBlock.engineer))
async def process_engineer_sent(callback: CallbackQuery, callback_data: ObjectCallbackFactory, state: FSMContext,
                                session: AsyncSession):
    await state.update_data(engineer_id=callback_data.id)
    data = await state.get_data()
    try:
        await orm_add_block(data, session)
        await callback.message.edit_text('➕ Узел добавлен.')
        await state.clear()
    except Exception as e:
        await callback.message.answer(f'Ошибка {e}')
        await state.clear()


@router_block.message(StateFilter(FSMFillBlock.engineer, FSMFillBlock.engineer))
async def warning_not_engineer(message: Message):
    await message.answer('Выберите инженера выше!\nОтменить внесение данных - /cancel')


@router_block.callback_query(BlockLookCallbackFactory.filter(), StateFilter(default_state))
async def process_list_get_object_block(callback: CallbackQuery, callback_data: ObjectCallbackFactory,
                                        session: AsyncSession):
    blocks = await orm_get_blocks_object(callback_data.id, session)
    await callback.message.delete()
    await callback.message.answer(text=f'🔻 {callback.message.text.split("Инженер")[0]}')
    for block in blocks:
        await callback.message.answer(text=f'Узел: {block.name}'
                                           f'\nИнженер: {block.engineer.firstname} {block.engineer.surname}'
                                           f'\nСтатус: {"✅ Проверен" if block.checked else "❌ Не проверен"}',
                                      reply_markup=await inline_kb_object_block(block))
