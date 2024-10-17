from telethon import TelegramClient
from app.config import settings

async def create_session(phone, api_id, api_hash):
    client = TelegramClient(phone, api_id, api_hash)
    await client.connect()
    return client

async def close_session(client):
    await client.disconnect()

# Implement other Telegram-related functions here