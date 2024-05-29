from aiogram.fsm.state import StatesGroup, State


class FSMFillEngineer(StatesGroup):
    user_id = State()
    firstname = State()
    surname = State()
    phone = State()


class FSMFillObject(StatesGroup):
    address = State()
    engineer = State()


class FSMFillBlock(StatesGroup):
    name = State()
    object = State()
    engineer = State()


class FSMFillCheckList(StatesGroup):
    scheme = State()
    one_c = State()
    equipment = State()
    location = State()
    optimal = State()
