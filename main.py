import asyncio
import os
from typing import List

import dotenv

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from database.engine import create_db, session_maker
from handlers.user_handlers_engineer import router_engineer
from handlers.user_handlers_object import router_object
from keyboards.set_menu import set_main_menu
from handlers.user_handlers_rules import router_rules
from middlewares.db import DataBaseSession

dotenv.load_dotenv()
allowed_updates: List[str] = []

bot = Bot(token=os.getenv('BOT_TOKEN'), default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()
dp.include_router(router_rules)
dp.include_router(router_engineer)
dp.include_router(router_object)


async def on_startup():
    await create_db()


async def on_shutdown():
    print('бот лег')


async def main():
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    dp.update.middleware(DataBaseSession(session_pool=session_maker))
    await bot.delete_webhook(drop_pending_updates=True)
    await set_main_menu(bot)
    await dp.start_polling(bot, allowed_updates=allowed_updates)


if __name__ == "__main__":
    asyncio.run(main())
