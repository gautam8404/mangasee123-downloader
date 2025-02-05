import os
from telethon import TelegramClient

api_id = os.environ.get('API_ID')
api_hash = os.environ.get('API_HASH')
bot_token = os.environ.get('BOT_TOKEN')
DATABASE = int(os.environ.get('DATABASE'))
CHANNEL_ID = int(os.environ.get('CHANNEL_ID'))

bot = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)