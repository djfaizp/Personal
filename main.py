import logging
import os
import asyncio
from telethon import TelegramClient, events
from telethon.tl.types import InputPeerUser, InputPeerChannel
from config import API_ID, API_HASH, BOT_TOKEN
from database.db_handler import DatabaseHandler
from plugins import load_plugins

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

class TelegramBot:
    def __init__(self, mode='bot'):
        self.mode = mode
        self.client = None
        self.db = DatabaseHandler()

    async def start(self):
        try:
            if self.mode == 'bot':
                self.client = TelegramClient('bot_session', API_ID, API_HASH).start(bot_token=BOT_TOKEN)
            else:
                self.client = TelegramClient('user_session', API_ID, API_HASH)
                await self.client.start()

                # If it's the first time, it will ask for phone and verification code
                if not await self.client.is_user_authorized():
                    phone = input("Enter your phone number (with country code): ")
                    await self.client.send_code_request(phone)
                    code = input("Enter the code you received: ")
                    await self.client.sign_in(phone, code)

            load_plugins(self.client, self.db)

            logger.info(f"Bot started in {self.mode} mode")
            await self.client.run_until_disconnected()
        except Exception as e:
            logger.error(f"Error starting bot: {str(e)}")

if __name__ == "__main__":
    mode = input("Enter login mode (bot/user): ").lower()
    if mode not in ['bot', 'user']:
        logger.warning("Invalid mode. Defaulting to bot mode.")
        mode = 'bot'

    bot = TelegramBot(mode)
    asyncio.run(bot.start())
