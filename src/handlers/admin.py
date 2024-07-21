from aiogram import Router

from config import bot, lock
from constants import BOT_OWNER_ID
from filters import AdminCommandFilter


router = Router(name=__name__)


@router.message(AdminCommandFilter('/skip'))
async def skip_command_handler(_):
    if lock.locked():
        await bot.send_message(
            chat_id=BOT_OWNER_ID,
            text='Сообщение скипнуто.'
        )
        return lock.release()
    await bot.send_message(
        chat_id=BOT_OWNER_ID,
        text='Сообщений больше нет.'
    )
