from telethon import TelegramClient
from config import settings
import logging

logger = logging.getLogger(__name__)

async def create_session(phone, api_id, api_hash):
    client = TelegramClient(phone, api_id, api_hash)
    try:
        await client.connect()
        if not await client.is_user_authorized():
            logger.error("El usuario no está autorizado. Verifica el número de teléfono y el código.")
            # Aquí puedes agregar lógica para manejar la autorización
        return client
    except Exception as e:
        logger.error("Error al crear la sesión: %s", e)
        return None

async def close_session(client):
    await client.disconnect()

# Implement other Telegram-related functions here