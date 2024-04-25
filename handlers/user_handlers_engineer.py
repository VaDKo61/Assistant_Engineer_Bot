from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import CallbackQuery, Message, InlineKeyboardButton, InlineKeyboardMarkup
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import Engineer
from database.orm_query import orm_add_engineer, orm_get_engineers, orm_get_engineer, orm_delete_engineer
from keyboards.keyboard_utils_engineer import inline_kb_engineer, EngineerCallbackFactory
from lexicon import replica
from states.states import FSMFillEngineer

router_engineer = Router()


@router_engineer.callback_query(F.data == 'engineer', StateFilter(default_state))
async def process_engineer(callback: CallbackQuery, session: AsyncSession):
    await callback.message.delete()
    for engineer in await orm_get_engineers(session):
        text_answer, keyboard = await inline_kb_engineer(engineer)
        await callback.message.answer(text=text_answer, reply_markup=keyboard)
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='+', callback_data='add_engineer')]])
    await callback.message.answer(text=replica.navigation['add_engineer'],
                                  reply_markup=keyboard)


@router_engineer.callback_query(EngineerCallbackFactory.filter(F.action == 'get'), StateFilter(default_state))
async def process_data_engineer(callback: CallbackQuery, session: AsyncSession, callback_data: EngineerCallbackFactory):
    engineer: Engineer = await orm_get_engineer(session, callback_data.id)
    await callback.message.answer('{} {}\n☎ {}'.format(engineer.firstname, engineer.surname, engineer.phone))


@router_engineer.callback_query(EngineerCallbackFactory.filter(F.action == 'del'), StateFilter(default_state))
async def process_delete_engineer(callback: CallbackQuery, session: AsyncSession,
                                  callback_data: EngineerCallbackFactory):
    await orm_delete_engineer(session, callback_data.id)
    await callback.answer('Инженер удален!')
    await callback.message.edit_text('❌ Инженер удален!')


@router_engineer.callback_query(F.data == 'add_engineer', StateFilter(default_state))
async def process_add_engineer_command(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer('Введите id инженера:')
    await state.set_state(FSMFillEngineer.user_id)


@router_engineer.message(StateFilter(FSMFillEngineer.user_id), F.text.isdigit())
async def process_user_id_sent(message: Message, state: FSMContext):
    await state.update_data(user_id=message.text)
    await message.answer('Введите имя инженера:')
    await state.set_state(FSMFillEngineer.firstname)


@router_engineer.message(StateFilter(FSMFillEngineer.user_id))
async def warning_not_user_id(message: Message):
    await message.answer('Вы ввели некорректный id!\nВедите id инженера.\nОтменить внесение данных - /cancel')


@router_engineer.message(StateFilter(FSMFillEngineer.firstname), F.text.isalpha())
async def process_firstname_sent(message: Message, state: FSMContext):
    await state.update_data(firstname=message.text)
    await message.answer('Введите фамилию инженера:')
    await state.set_state(FSMFillEngineer.surname)


@router_engineer.message(StateFilter(FSMFillEngineer.firstname))
async def warning_not_firstname(message: Message):
    await message.answer('Вы ввели некорректное имя!\nВедите имя инженера.\nОтменить внесение данных - /cancel')


@router_engineer.message(StateFilter(FSMFillEngineer.surname), F.text.isalpha())
async def process_surname_sent(message: Message, state: FSMContext):
    await state.update_data(surname=message.text)
    await message.answer('Введите номер телефона инженера:')
    await state.set_state(FSMFillEngineer.phone)


@router_engineer.message(StateFilter(FSMFillEngineer.surname))
async def warning_not_surname(message: Message):
    await message.answer(
        'Вы ввели некорректное фамилию!\nВедите фамилию инженера.\nОтменить внесение данных - /cancel')


@router_engineer.message(StateFilter(FSMFillEngineer.phone), F.text.isdigit())
async def process_phone_sent(message: Message, state: FSMContext, session: AsyncSession):
    await state.update_data(phone=message.text)
    data = await state.get_data()
    try:
        await orm_add_engineer(session, data)
        await message.answer('➕ Инженер добавлен.')
        await state.clear()
    except Exception as e:
        await message.answer(f'Ошибка {e}')
        await state.clear()


@router_engineer.message(StateFilter(FSMFillEngineer.phone))
async def warning_not_phone(message: Message):
    await message.answer(
        'Вы ввели некорректный номер!\nВедите номер телефона инженера.\nОтменить внесение данных - /cancel')
