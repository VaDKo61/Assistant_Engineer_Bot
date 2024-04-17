from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery, FSInputFile

from handlers.process_rules import get_rules, get_rules_read
from keyboards.keyboard_utils import inline_kb_rules, RulesCallbackFactory, RulesReadCallbackFactory
from lexicon import replica

router = Router()


@router.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(replica.information['greet'].format(name=message.from_user.full_name))
    await message.answer('\n'.join([f'/{i} - {j}' for i, j in replica.commands.items()]))


@router.message(Command('rules'))
async def process_rules_command(message: Message):
    await message.answer(text=replica.navigation['category'],
                         reply_markup=inline_kb_rules(0))


@router.callback_query(RulesCallbackFactory.filter())
async def process_rules(callback: CallbackQuery, callback_data: RulesCallbackFactory):
    """handler for rules"""
    if callback_data.level == -1:
        await callback.message.delete()
    elif callback_data.level == -2:
        await callback.message.delete()
        path: str = r'Z:\Библиотека Solid Works НОВАЯ\Внутренние правила для конструкторов при сборке БТП.docx'
        await callback.message.answer_document(FSInputFile(path))
    else:
        text_answer, keyboard = get_rules(callback_data)
        await callback.message.edit_text(text=text_answer, reply_markup=keyboard)
    await callback.answer()


@router.callback_query(RulesReadCallbackFactory.filter())
async def process_read_rules(callback: CallbackQuery, callback_data: RulesReadCallbackFactory):
    """handler for read rules"""
    text_answer, keyboard = get_rules_read(callback_data)
    await callback.message.edit_text(text=text_answer, reply_markup=keyboard)
    await callback.answer()
