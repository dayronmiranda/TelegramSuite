from telethon import TelegramClient
from config import settings
from utils.file_utils import process_media_file
import os

async def download_media(client: TelegramClient, message, media_directory: str):
    if message.media:
        file_path = os.path.join(media_directory, f"{message.id}_{message.media.id}")
        try:
            downloaded_file = await client.download_media(message, file=file_path)
            if downloaded_file:
                processed_file = await process_media_file(downloaded_file)
                return {
                    "type": str(type(message.media).__name__),
                    "file_path": processed_file,
                }
        except Exception as e:
            # Log the error here
            return None
    return None

async def download_media_batch(client: TelegramClient, messages, media_directory: str):
    media_info = []
    for message in messages:
        media_data = await download_media(client, message, media_directory)
        if media_data:
            media_info.append({
                "message_id": message.id,
                "media": media_data
            })
    return media_info