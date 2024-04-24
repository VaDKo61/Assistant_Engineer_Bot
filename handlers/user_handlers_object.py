from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import CallbackQuery, Message

from states.states import FSMFillObject

router_object = Router()


@router_object.callback_query(F.data == 'add_object', StateFilter(default_state))
async def process_add_object_command(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer('Введите адрес объекта:')
    await state.set_state(FSMFillObject.address)


@router_object.message(StateFilter(FSMFillObject.address), F.text.isalpha())
async def process_address_sent(message: Message, state: FSMContext):
    await message.answer('Введите ответственного за объект:')
    await state.set_state(FSMFillObject.responsible)


@router_object.message(StateFilter(FSMFillObject.address))
async def warning_not_address(message: Message):
    await message.answer('Вы ввели некорректный адрес!\nВедите адрес объекта.\nОтменить внесение данных - /cancel')

# @router.message(StateFilter(FSMFillObjects.fill_responsible), F.text.isalpha())
