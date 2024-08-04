from aiogram.fsm.state import State, StatesGroup


class SetChatStates(StatesGroup):
    chat_id = State()
