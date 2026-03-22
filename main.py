import asyncio
from aiogram import Bot, Dispatcher
from config import bot_token
from bot.handlers import router

async def main():
    bot = Bot(token=bot_token)

    dp = Dispatcher()
    dp.include_router(router)

    print("Бот успешно запущен и готов к работе!")
    
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())