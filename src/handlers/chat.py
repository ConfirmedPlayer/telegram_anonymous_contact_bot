from aiogram import Router, html
from aiogram.types import Message
from loguru import logger

from config import bot, dp
from constants import BOT_OWNER_ID

router = Router(name=__name__)


@router.message(lambda event: event.from_user.id != BOT_OWNER_ID)
async def user_message_handler(msg: Message) -> None:
    user_id = f'{msg.from_user.id}'
    message_text = msg.text or 'empty message'

    logger.info({user_id: message_text})

    await bot.send_message(
        chat_id=BOT_OWNER_ID,
        text=f'Новое сообщение от "{msg.from_user.full_name}" ({html.code(msg.from_user.id)}):',
    )

    await msg.forward(BOT_OWNER_ID)

    await bot.send_message(
        chat_id=BOT_OWNER_ID,
        text='Используйте команду /set_chat чтобы установить диалог с пользователем.',
    )

    if chat_id := await dp.storage.get_data('chat_id'):
        await bot.send_message(
            chat_id=BOT_OWNER_ID,
            text=f'Сейчас установлен диалог с пользователем с id: {html.code(chat_id["id"])}',
        )
    else:
        await bot.send_message(
            chat_id=BOT_OWNER_ID,
            text='Сейчас ни с каким пользователем не установлен диалог.',
        )


@router.message(
    lambda event: all(
        (
            event.from_user.id == BOT_OWNER_ID,
            not event.text.startswith('/') if event.text else True,
        )
    )
)
async def admin_message_handler(msg: Message) -> None:
    if chat_id := await dp.storage.get_data('chat_id'):
        await msg.forward(chat_id=chat_id['id'])
        await bot.send_message(
            chat_id=BOT_OWNER_ID,
            text=f'Сообщение отправлено пользователю с id: {html.code(chat_id["id"])}',
        )
