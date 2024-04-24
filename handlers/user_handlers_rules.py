from aiogram import Router
from aiogram.filters import CommandStart, Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message, CallbackQuery, FSInputFile

from handlers.process_rules import get_rules, get_rules_read
from keyboards.keyboard_utils_rules import inline_kb_rules, RulesCallbackFactory, RulesReadCallbackFactory, \
    inline_kb_menu
from lexicon import replica

router_rules = Router()


@router_rules.message(CommandStart(), StateFilter(default_state))
async def process_start_command(message: Message):
    await message.answer(replica.information['greet'].format(name=message.from_user.full_name))
    await message.answer('\n'.join([f'/{i} - {j}' for i, j in replica.commands.items()]))


@router_rules.message(Command('menu'), StateFilter(default_state))
async def process_menu_command(message: Message):
    await message.answer(text=replica.navigation['menu'], reply_markup=inline_kb_menu())


@router_rules.message(Command('rules'), StateFilter(default_state))
async def process_rules_command(message: Message):
    await message.answer(text=replica.navigation['category'], reply_markup=inline_kb_rules(0))


@router_rules.callback_query(RulesCallbackFactory.filter(), StateFilter(default_state))
async def process_rules(callback: CallbackQuery, callback_data: RulesCallbackFactory):
    """handler for rules"""
    if callback_data.level == -1:
        await callback.message.delete()
    elif callback_data.level == -2:
        await callback.message.delete()
        path: str = r'Z:\Библиотека Solid Works НОВАЯ\Внутренние правила для конструкторов при сборке БТП.docx'
        await callback.message.answer_document(FSInputFile(path))
    else:
        text_answer, keyboard = await get_rules(callback_data)
        await callback.message.edit_text(text=text_answer, reply_markup=keyboard)
    await callback.answer()


@router_rules.callback_query(RulesReadCallbackFactory.filter(), StateFilter(default_state))
async def process_read_rules(callback: CallbackQuery, callback_data: RulesReadCallbackFactory):
    """handler for read rules"""
    text_answer, keyboard = await get_rules_read(callback_data)
    await callback.message.edit_text(text=text_answer, reply_markup=keyboard)
    await callback.answer()


@router_rules.message(Command('cancel'), StateFilter(default_state))
async def process_cancel_command(message: Message):
    await message.answer('Вы не заносите данные, откройте /menu')


@router_rules.message(Command('cancel'), ~StateFilter(default_state))
async def process_cancel_command_state(message: Message, state: FSMContext):
    await message.answer('Вы отменили внесение данных.')
    await state.clear()


# routers for checklist
@router_rules.message(Command('checklist'), StateFilter(default_state))
async def process_checklist_command(message: Message):
    await message.answer('asd')
