from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import Update
from bot.database.helper import Database


class DBMiddleware(BaseMiddleware):
    def __init__(self, sessionmaker) -> None:
        self.sessionmaker = sessionmaker

    async def __call__(
            self,
            handler: Callable[[Update, Dict[str, Any]], Awaitable[Any]],
            update: Update,
            data: Dict[str, Any],
    ) -> Any:
        async with self.sessionmaker() as session:
            data["session"] = Database(session)
            return await handler(update, data)
