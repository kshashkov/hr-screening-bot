from aiogram import Router
from aiogram.filters import Filter
from aiogram.types import Message

from bot import settings

router = Router()

HR_IDS = settings.Settings().HR_IDS


class HRFilter(Filter):
    async def __call__(self, message: Message) -> bool:
        return message.from_user.id in HR_IDS
