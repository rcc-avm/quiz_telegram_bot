import asyncio
from aiogram import Bot, Dispatcher
from handlers import quiz_handlers, start_handler
from utils.db_utils import create_tables
from config import TELEGRAM_BOT_TOKEN

bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher()

async def main():
    await create_tables()
    dp.include_router(quiz_handlers.router)
    dp.include_router(start_handler.router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
