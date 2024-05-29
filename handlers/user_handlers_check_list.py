from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import CallbackQuery, Message
from sqlalchemy.ext.asyncio import AsyncSession

from database.orm_query import orm_get_object, orm_add_check_list
from keyboards.keyboard_utils_check_list import inline_kb_check
from keyboards.keyboard_utils_object_block import BlockCheckCallbackFactory
from states.states import FSMFillCheckList

router_check_list = Router()


@router_check_list.callback_query(BlockCheckCallbackFactory.filter(), StateFilter(default_state))
async def process_check_block_command(callback: CallbackQuery, callback_data: BlockCheckCallbackFactory,
                                      state: FSMContext, session: AsyncSession):
    await state.update_data(block_id=callback_data.id)
    obj = await orm_get_object(session, callback_data.object_id)
    await callback.message.answer(f'Объект: <b><u>{obj.address}</u></b>\n'
                                  f'Проверяем узел: <b>{callback_data.name}</b>')
    await callback.message.answer(text='Узел совпадает с принципиальной схемой?',
                                  reply_markup=await inline_kb_check('check_scheme'))
    await state.set_state(FSMFillCheckList.scheme)


@router_check_list.callback_query(StateFilter(FSMFillCheckList.scheme), F.data == 'check_scheme')
async def process_scheme_sent(callback: CallbackQuery, state: FSMContext):
    await state.update_data(scheme=True)
    await callback.message.edit_text(text='Узел совпадает с 1C?',
                                     reply_markup=await inline_kb_check('check_one_c'))
    await state.set_state(FSMFillCheckList.one_c)


@router_check_list.callback_query(
    StateFilter(FSMFillCheckList.scheme, FSMFillCheckList.one_c, FSMFillCheckList.location, FSMFillCheckList.equipment,
                FSMFillCheckList.optimal),
    F.data == 'check_cancel')
async def process_check_cancel(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.answer('Вы отменили проверку')


@router_check_list.message(
    StateFilter(FSMFillCheckList.scheme, FSMFillCheckList.one_c, FSMFillCheckList.location, FSMFillCheckList.equipment,
                FSMFillCheckList.optimal))
async def warning_not_equipment(message: Message):
    await message.answer('Выберите ответ выше!\nОтменить внесение данных - /cancel')


@router_check_list.callback_query(StateFilter(FSMFillCheckList.one_c), F.data == 'check_one_c')
async def process_one_c_sent(callback: CallbackQuery, state: FSMContext):
    await state.update_data(one_c=True)
    await callback.message.edit_text(text='Оборудование расположено верно?',
                                     reply_markup=await inline_kb_check('check_equipment'))
    await state.set_state(FSMFillCheckList.equipment)


@router_check_list.callback_query(StateFilter(FSMFillCheckList.equipment), F.data == 'check_equipment')
async def process_equipment_sent(callback: CallbackQuery, state: FSMContext):
    await state.update_data(equipment=True)
    await callback.message.edit_text(text='Блок в помещении расположен верно?',
                                     reply_markup=await inline_kb_check('check_location'))
    await state.set_state(FSMFillCheckList.location)


@router_check_list.callback_query(StateFilter(FSMFillCheckList.location), F.data == 'check_location')
async def process_location_sent(callback: CallbackQuery, state: FSMContext):
    await state.update_data(location=True)
    await callback.message.edit_text(text='Блок с оптимальным техническим решением?',
                                     reply_markup=await inline_kb_check('check_optimal'))
    await state.set_state(FSMFillCheckList.optimal)


@router_check_list.callback_query(StateFilter(FSMFillCheckList.optimal), F.data == 'check_optimal')
async def process_optimal_sent(callback: CallbackQuery, state: FSMContext, session: AsyncSession):
    await state.update_data(optimal=True)
    data = await state.get_data()
    try:
        await orm_add_check_list(data, session)
        await callback.message.edit_text('✅ Блок проверен.')
        await state.clear()
    except Exception as e:
        await callback.message.answer(f'Ошибка {e}')
        await state.clear()