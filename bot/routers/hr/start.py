from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from bot.database.helper import Database
from bot.filters.hr import HRFilter

router = Router()
router.message.filter(HRFilter())


@router.message(CommandStart())
async def start(message: Message, session: Database):
    try:
        await session.add_user(message.from_user.id, message.from_user.username)
    except:
        pass
    await message.answer("Welcome!\nUse /generate to generate a questionnaire for your job description.")
