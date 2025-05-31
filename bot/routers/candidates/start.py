from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

router = Router()

from bot.database.helper import Database


@router.message(CommandStart())
async def start(message: Message, session: Database):
    try:
        await message.answer("Welcome")
        await session.add_user(message.from_user.id, message.from_user.username)
    except:
        await message.answer("An error has occurred. It seems like you are not a registered user.")
        pass
    await message.answer("Please contact your HR manager to access the bot.")
