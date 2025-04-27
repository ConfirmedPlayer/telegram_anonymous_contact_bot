from aiogram.filters import Filter
from aiogram.types import Message

from constants import BOT_OWNER_ID


class AdminCommandFilter(Filter):
    def __init__(
        self, command: str, admin_user_id: int = BOT_OWNER_ID
    ) -> None:
        self.command = command
        self.admin_user_id = admin_user_id

    async def __call__(self, msg: Message) -> bool:
        if msg.from_user.id == self.admin_user_id:
            if msg.text and msg.text.startswith(self.command):
                return True
        return False
