from aiogram.fsm.state import State, StatesGroup


class Login(StatesGroup):
    secret_key = State()
