from aiogram import Router, F
from aiogram.enums import ContentType
from aiogram.filters import StateFilter, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import CallbackQuery, Message
from sqlalchemy.ext.asyncio import AsyncSession

from database.orm_query import orm_add_object, orm_get_objects_checked
from keyboards.keyboard_utils_object_block import inline_kb_choose_engineer, ObjectCallbackFactory, inline_kb_look_block
from states.states import FSMFillObject, FSMFillBlock

router_object = Router()


@router_object.callback_query(F.data == 'add_object', StateFilter(default_state))
async def process_add_object_command(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text('Введите адрес объекта:')
    await state.set_state(FSMFillObject.address)


@router_object.message(Command('add_object'), StateFilter(default_state))
async def process_add_object_menu(message: Message, state: FSMContext):
    await message.answer('Введите адрес объекта:')
    await state.set_state(FSMFillObject.address)


@router_object.message(StateFilter(FSMFillObject.address), F.content_type == ContentType.TEXT)
async def process_address_sent(message: Message, state: FSMContext, session: AsyncSession):
    await state.update_data(address=message.text)
    await message.answer(text='Выберите ответственного за объект:',
                         reply_markup=await inline_kb_choose_engineer(session))
    await state.set_state(FSMFillObject.engineer)


@router_object.message(StateFilter(FSMFillObject.address))
async def warning_not_address(message: Message):
    await message.answer('Вы ввели некорректный адрес!\nВедите адрес объекта.\nОтменить внесение данных - /cancel')


@router_object.callback_query(ObjectCallbackFactory.filter(), StateFilter(FSMFillObject.engineer))
async def process_engineer_sent(callback: CallbackQuery, callback_data: ObjectCallbackFactory, state: FSMContext,
                                session: AsyncSession):
    await state.update_data(engineer_id=callback_data.id)
    data = await state.get_data()
    try:
        await orm_add_object(session, data)
        await callback.message.answer('➕ Объект добавлен.')
        await state.clear()
    except Exception as e:
        await callback.message.answer(f'Ошибка {e}')
        await state.clear()


@router_object.message(StateFilter(FSMFillObject.engineer, FSMFillBlock.engineer))
async def warning_not_engineer(message: Message):
    await message.answer('Выберите инженера выше!\nОтменить внесение данных - /cancel')


@router_object.callback_query(F.data == 'list_object_checked', StateFilter(default_state))
async def process_list_get_object_checked(callback: CallbackQuery, session: AsyncSession):
    list_obj: list[str] = []
    for obj in await orm_get_objects_checked(session, True):
        block = [f'<b>{i.name}</b> - {i.engineer.firstname} {i.engineer.surname}' for i in obj.blocks]
        list_obj.append(f'<b><u>{obj.address}</u></b>\n'
                        f'Инженер: {obj.engineer.firstname} {obj.engineer.surname}\n'
                        f'Узлы: {"; ".join(block)}')
    await callback.message.edit_text('\n'.join(list_obj))


@router_object.callback_query(F.data == 'list_object_unchecked', StateFilter(default_state))
async def process_list_get_object_unchecked(callback: CallbackQuery, session: AsyncSession):
    await callback.message.delete()
    for obj in await orm_get_objects_checked(session, False):
        await callback.message.answer(
            text=f'<b>{obj.address}</b>\nИнженер: {obj.engineer.firstname} {obj.engineer.surname}',
            reply_markup=await inline_kb_look_block(obj))
