from aiogram import Router
from aiogram.types import Message
from loguru import logger

from config import bot, dp, lock
from constants import BOT_OWNER_ID


router = Router(name=__name__)


@router.message(lambda event: event.from_user.id != BOT_OWNER_ID)
async def user_message_handler(msg: Message) -> None:
    await lock.acquire()

    user_id = f'{msg.from_user.id}'
    message_text = msg.text or 'empty message'

    logger.info(
        {user_id: message_text}
    )

    await dp.storage.set_data('latest_user', {'user_id': msg.from_user.id})

    await bot.send_message(
        chat_id=BOT_OWNER_ID,
        text=f'Новое сообщение от "{msg.from_user.full_name}" ({msg.from_user.id}):'
    )

    await msg.forward(BOT_OWNER_ID)

    await bot.send_message(
        chat_id=BOT_OWNER_ID,
        text='Отправьте команду /skip для того чтобы оставить сообщение без ответа.'
    )


@router.message(lambda event: all(
    (
        event.from_user.id == BOT_OWNER_ID,
        not event.text.startswith('/') if event.text else True
    )
))
async def admin_message_handler(msg: Message) -> None:
    try:
        if latest_user := await dp.storage.get_data('latest_user'):
            await msg.send_copy(chat_id=latest_user['user_id'])
    finally:
        if lock.locked():
            lock.release()
