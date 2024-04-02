from aiogram import Router, F
from aiogram.filters import CommandStart, Command, or_f
from aiogram.types import Message

from keyboards import keyboard_utils
from lexicon import text

router = Router()


@router.message(CommandStart())
async def start_handler(message: Message):
    await message.answer(text.greet.format(name=message.from_user.full_name), reply_markup=keyboard_utils.menu)


@router.message(or_f(Command('buy'), (F.text.lower().contains('купит'))))
async def echo(message: Message):
    await message.answer('Раздел: Купить', reply_markup=keyboard_utils.menu)


@router.message(or_f(Command('sell'), (F.text.lower().contains('прода'))))
async def echo(message: Message):
    await message.answer('Раздел: Купить')


@router.message(or_f(Command('info'), (F.text.lower().contains('информация'))))
async def echo(message: Message):
    [await message.answer(f'{i}') for i in text.info]
