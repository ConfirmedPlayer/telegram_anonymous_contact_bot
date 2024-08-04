import asyncio
import sys

from aiogram import html
from aiogram.filters import CommandStart
from aiogram.types import ErrorEvent, Message
from loguru import logger

from config import bot, dp
from constants import BOT_OWNER_ID, BOT_OWNER_NICKNAME
from handlers import routers


@dp.message(CommandStart())
async def command_start_handler(msg: Message) -> None:
    if msg.from_user.id == BOT_OWNER_ID:
        await msg.answer('Вы админ этого бота. Скоро будете получать сообщения!')
        return

    user_full_name = html.bold(msg.from_user.full_name)
    greeting = (
        f'Привет, {user_full_name}!\n\n'
        f'Здесь ты можешь написать что угодно, и это увидит @{BOT_OWNER_NICKNAME}.\n\n'
        'Таким образом, ты можешь анонимно связаться с этим человеком.'
    )

    await msg.answer(greeting)


@dp.error()
async def telegram_error_handler(event: ErrorEvent) -> None:
    logger.exception(f'New exception by telegram error handler: {event.exception}')
    await bot.send_message(
        chat_id=BOT_OWNER_ID,
        text=f'Ошибка!\n\n{event.exception}'
    )


async def main() -> None:
    dp.include_routers(*routers)
    await dp.start_polling(bot)


if __name__ == '__main__':
    logger.add(sink='logs.log', level='INFO')
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        sys.exit(0)
