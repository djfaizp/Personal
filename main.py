import logging
import asyncio
from telethon import TelegramClient
from config import API_ID, API_HASH, BOT_TOKEN
from database.db_handler import DatabaseHandler
from plugins import load_plugins

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

class TelegramBot:
    def __init__(self):
        self.client = None
        self.db = DatabaseHandler()

    async def start(self):
        try:
            # Always start in bot mode
            self.client = TelegramClient('bot_session', API_ID, API_HASH).start(bot_token=BOT_TOKEN)

            # Load plugins
            load_plugins(self.client, self.db)

            logger.info("Bot started successfully")

            # Run the client until disconnected
            await self.client.run_until_disconnected()
        except Exception as e:
            logger.error(f"Error starting bot: {str(e)}")

if __name__ == "__main__":
    bot = TelegramBot()
    asyncio.run(bot.start())
