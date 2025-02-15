import asyncio
from assistant.core.bot import Bot
from assistant.utils.logger import logger

async def main():
    """Запуск голосового ассистента"""
    bot = Bot()
    await bot.start()

if __name__ == "__main__":
    logger.info("🚀 Запуск голосового ассистента...")
    asyncio.run(main())