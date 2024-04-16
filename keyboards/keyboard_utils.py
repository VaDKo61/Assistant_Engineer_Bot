from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from lexicon import text


class RulesCallbackFactory(CallbackData, prefix='id'):
    level: int
    category: int
    subcategory: float


def inline_kb_rules(level: int, category: int = 0, subcategory: float = 0, width: int = 1) -> InlineKeyboardMarkup:
    """create a built-in keyboard rules depending on the level"""
    kb_builder = InlineKeyboardBuilder()
    buttons: list[InlineKeyboardButton] = []
    last_btns: list[InlineKeyboardButton] = []
    back = ('↩ Назад', RulesCallbackFactory(level=level - 1, category=category, subcategory=subcategory))
    close = ('❌ Закрыть правила', RulesCallbackFactory(level=-1, category=0, subcategory=0))
    if level == 0:
        for key in text.rules.keys():
            buttons.append(InlineKeyboardButton(text=str('{}. {}'.format(key, ''.join(text.rules_description[key]))),
                                                callback_data=RulesCallbackFactory(level=level + 1,
                                                                                   category=key,
                                                                                   subcategory=subcategory).pack()))
    elif level == 1:
        for key, value in text.rules[category].items():
            buttons.append(InlineKeyboardButton(text=str('{}. {}'.format(key, ''.join(value))),
                                                callback_data=RulesCallbackFactory(level=level + 1,
                                                                                   category=category,
                                                                                   subcategory=key).pack()))
        buttons.append(InlineKeyboardButton(text='📖 Читать все правила данного раздела', callback_data='read'))
        last_btns.append(InlineKeyboardButton(text=back[0], callback_data=back[1].pack()))
    else:
        last_btns.append(InlineKeyboardButton(text=back[0], callback_data=back[1].pack()))
    last_btns.append(InlineKeyboardButton(text=close[0], callback_data=close[1].pack()))
    kb_builder.row(*buttons, width=width)
    kb_builder.row(*last_btns, width=2)
    return kb_builder.as_markup()
