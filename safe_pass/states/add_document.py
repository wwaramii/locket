from aiogram.fsm.state import State, StatesGroup


class AddDocument(StatesGroup):
    title = State()
    document_pack_identifier = State()
    data = State()
