from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery

from handlers.process_rules import get_rules
from keyboards.keyboard_utils import inline_kb_rules, RulesCallbackFactory
from lexicon import text

router = Router()


@router.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(text.information['greet'].format(name=message.from_user.full_name))
    await message.answer('\n'.join([f'/{i} - {j}' for i, j in text.commands.items()]))


@router.message(Command('rules'))
async def process_rules_command(message: Message):
    await message.answer(text='Выберите раздел:',
                         reply_markup=inline_kb_rules(0))


@router.callback_query(RulesCallbackFactory.filter())
async def process_rules(callback: CallbackQuery, callback_data: RulesCallbackFactory):
    """handler for rules"""
    if callback_data.level == -1:
        await callback.message.delete()
    else:
        text_answer, keyboard = get_rules(callback_data)
        await callback.message.edit_text(text=text_answer, reply_markup=keyboard)
    await callback.answer()
