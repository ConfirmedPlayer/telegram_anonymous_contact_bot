from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from config import dp
from filters import AdminCommandFilter
from states import SetChatStates


router = Router(name=__name__)


@router.message(AdminCommandFilter('/ping'))
async def ping_command_handler(msg: Message) -> None:
    await msg.answer('pong')


@router.message(AdminCommandFilter('/set_chat'))
async def set_chat_command_handler(msg: Message, state: FSMContext) -> None:
    await state.set_state(SetChatStates.chat_id)
    await msg.answer('Скопируйте и отправьте айди пользователя, с кем хотите поговорить.')


@router.message(SetChatStates.chat_id)
async def set_chat_state_handler(msg: Message, state: FSMContext) -> None:
    await dp.storage.set_data('chat_id', {'id': int(msg.text)})
    await msg.answer(f'Диалог установлен с пользователем: {msg.text}')
    await state.clear()
