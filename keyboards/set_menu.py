from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeAllPrivateChats

from lexicon.text import commands


async def set_main_menu(bot: Bot):
    main_menu_commands = [BotCommand(command=command, description=description) for command, description in
                          commands.items()]
    await bot.set_my_commands(main_menu_commands, scope=BotCommandScopeAllPrivateChats())
