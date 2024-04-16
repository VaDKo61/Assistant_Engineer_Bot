from aiogram.types import InlineKeyboardMarkup

from keyboards.keyboard_utils import RulesCallbackFactory, inline_kb_rules

from lexicon import text


def get_rules(callback_data: RulesCallbackFactory) -> (str, InlineKeyboardMarkup):
    """get a text for answer, and a built-in keyboard depending on the level"""
    if callback_data.level == 0:
        text_answer = 'Выберите раздел:'
        keyboard = inline_kb_rules(level=0)
    elif callback_data.level == 1:
        text_answer = 'Выберите подраздел:'
        keyboard = inline_kb_rules(level=1, category=callback_data.category)
    else:
        rule = text.rules[callback_data.category][callback_data.subcategory]
        text_answer = str('{}. {}'.format(callback_data.subcategory, ''.join(rule)))
        keyboard = inline_kb_rules(level=2, category=callback_data.category, subcategory=callback_data.subcategory)
    return text_answer, keyboard
