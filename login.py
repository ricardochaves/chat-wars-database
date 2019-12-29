from chat_wars_database.settings import TELEGRAM_API_HASH
from chat_wars_database.settings import TELEGRAM_API_ID
from telethon import TelegramClient
from telethon.sessions import StringSession

with TelegramClient(StringSession(), TELEGRAM_API_ID, TELEGRAM_API_HASH) as client:
    print(client.session.save())
