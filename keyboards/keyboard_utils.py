from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from lexicon import replica, rules


class RulesCallbackFactory(CallbackData, prefix='id'):
    level: int
    category: int
    subcategory: int


class RulesReadCallbackFactory(CallbackData, prefix='read'):
    category: int
    subcategory: int


def inline_kb_rules(level: int, category: int = 0, subcategory: float = 0, width: int = 1) -> InlineKeyboardMarkup:
    """create a built-in keyboard rules depending on the level"""
    kb_builder = InlineKeyboardBuilder()
    buttons: list[InlineKeyboardButton] = []
    last_btns: list[InlineKeyboardButton] = []
    back = (
        replica.navigation['back'], RulesCallbackFactory(level=level - 1, category=category, subcategory=subcategory))
    close = (replica.navigation['close_rule'], RulesCallbackFactory(level=-1, category=0, subcategory=0))
    if level == 0:
        for key in rules.rules.keys():
            buttons.append(InlineKeyboardButton(text=str('{}. {}'.format(key, ''.join(rules.rules_description[key]))),
                                                callback_data=RulesCallbackFactory(level=level + 1,
                                                                                   category=key,
                                                                                   subcategory=subcategory).pack()))
        buttons.append(InlineKeyboardButton(text=replica.navigation['get_rules'],
                                            callback_data=RulesCallbackFactory(level=-2,
                                                                               category=0,
                                                                               subcategory=0).pack()))
    elif level == 1:
        for key, value in rules.rules[category].items():
            buttons.append(InlineKeyboardButton(text=str('{}.{}. {}'.format(category, key, ''.join(value))),
                                                callback_data=RulesCallbackFactory(level=level + 1,
                                                                                   category=category,
                                                                                   subcategory=key).pack()))
        buttons.append(InlineKeyboardButton(text=replica.navigation['read_rule'],
                                            callback_data=RulesReadCallbackFactory(category=category,
                                                                                   subcategory=1).pack()))
        last_btns.append(InlineKeyboardButton(text=back[0], callback_data=back[1].pack()))
    else:
        last_btns.append(InlineKeyboardButton(text=back[0], callback_data=back[1].pack()))
    last_btns.append(InlineKeyboardButton(text=close[0], callback_data=close[1].pack()))
    kb_builder.row(*buttons, width=width)
    kb_builder.row(*last_btns, width=2)
    return kb_builder.as_markup()


def inline_kb_rules_read(category: int, subcategory: int) -> InlineKeyboardMarkup:
    """create a built-in keyboard rules depending on rule"""
    kb_builder = InlineKeyboardBuilder()
    buttons_1: list[InlineKeyboardButton] = []
    buttons_2: list[InlineKeyboardButton] = []
    buttons_1.append(InlineKeyboardButton(text=replica.navigation['get_other'],
                                          callback_data=RulesCallbackFactory(level=0,
                                                                             category=0,
                                                                             subcategory=0).pack()))
    buttons_2.append(InlineKeyboardButton(text=replica.navigation['back'],
                                          callback_data=RulesReadCallbackFactory(category=category,
                                                                                 subcategory=subcategory - 1).pack()))
    buttons_2.append(InlineKeyboardButton(text=replica.navigation['close_rule'],
                                          callback_data=RulesCallbackFactory(level=-1, category=0,
                                                                             subcategory=0).pack()))
    buttons_2.append(InlineKeyboardButton(text=replica.navigation['forward'],
                                          callback_data=RulesReadCallbackFactory(category=category,
                                                                                 subcategory=subcategory + 1).pack()))
    if subcategory <= 1:
        buttons_2 = buttons_2[1:]
    elif subcategory >= len(rules.rules[category]):
        buttons_2 = buttons_2[:-1]
    kb_builder.row(*buttons_1, width=1)
    kb_builder.row(*buttons_2, width=3)
    return kb_builder.as_markup()
