import aiohttp
from utils.logging import logger
from config import settings

async def send_webhook_notification(url: str, data: dict):
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(url, json=data, timeout=settings.WEBHOOK_TIMEOUT) as response:
                if response.status != 200:
                    logger.error(f"Error sending webhook notification. Status: {response.status}")
        except Exception as e:
            logger.error(f"Error sending webhook notification: {str(e)}")