from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import CallbackQuery, Message
from sqlalchemy.ext.asyncio import AsyncSession

from database.orm_query import orm_add_object
from keyboards.keyboard_utils_object import inline_kb_choose_engineer, ObjectCallbackFactory
from states.states import FSMFillObject

router_object = Router()


@router_object.callback_query(F.data == 'add_object', StateFilter(default_state))
async def process_add_object_command(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer('Введите адрес объекта:')
    await state.set_state(FSMFillObject.address)


@router_object.message(StateFilter(FSMFillObject.address), F.text.isalnum())
async def process_address_sent(message: Message, state: FSMContext, session: AsyncSession):
    await state.update_data(address=message.text)
    await message.answer(text='Выберите ответственного за объект:',
                         reply_markup=await inline_kb_choose_engineer(session))
    await state.set_state(FSMFillObject.engineer)


@router_object.message(StateFilter(FSMFillObject.address))
async def warning_not_address(message: Message):
    await message.answer('Вы ввели некорректный адрес!\nВедите адрес объекта.\nОтменить внесение данных - /cancel')


@router_object.callback_query(ObjectCallbackFactory.filter())
async def process_engineer_sent(callback: CallbackQuery, state: FSMContext, session: AsyncSession):
    await state.update_data(engineer_id=callback.message.text)
    data = await state.get_data()
    try:
        await orm_add_object(session, data)
        await callback.message.answer('➕ Объект добавлен.')
        await state.clear()
    except Exception as e:
        await callback.message.answer(f'Ошибка {e}')
        await state.clear()


@router_object.message(StateFilter(FSMFillObject.engineer))
async def warning_not_engineer(message: Message):
    await message.answer('Выберите инженера выше!\nОтменить внесение данных - /cancel')
