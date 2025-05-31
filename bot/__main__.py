import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from bot.middlewares.db import DBMiddleware
from bot.settings import Settings


def setup_routes(dp):
    import bot.routers.hr
    import bot.routers.candidates

    dp.include_routers(bot.routers.candidates.questions_router)
    dp.include_routers(bot.routers.hr.start_router)
    # dp.include_routers(bot.routers.hr.config_router)
    dp.include_routers(bot.routers.hr.generate_router)
    dp.include_routers(bot.routers.candidates.start_router)


async def setup_db():
    from bot.database.base import Base
    from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

    settings = Settings()
    engine = create_async_engine(settings.DATABASE_URL.get_secret_value())
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    async_session = async_sessionmaker(engine, expire_on_commit=False)
    return async_session


async def main() -> None:
    logging.info("Starting the bot")
    settings = Settings()

    sessionmaker = await setup_db()

    bot = Bot(token=settings.BOT_TOKEN.get_secret_value(), default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()

    setup_routes(dp)
    dp.update.middleware(DBMiddleware(sessionmaker))


    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
