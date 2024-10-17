import asyncio
from aiokafka import AIOKafkaConsumer
import json
from config import settings
from database.mongodb import get_db, init_mongodb
from services.media_service import download_media
from telethon import TelegramClient

async def process_media(message):
    db = get_db()
    media_data = json.loads(message.value)
    session_data = media_data['session_data']
    
    client = TelegramClient(session_data["phone"], session_data["api_id"], session_data["api_hash"])
    await client.start()
    
    try:
        message = await client.get_messages(media_data['chat_id'], ids=media_data['message_id'])
        media_info = await download_media(client, message, settings.MEDIA_DIRECTORY)
        
        if media_info:
            await db.messages.update_one(
                {"message_id": media_data['message_id'], "chat_id": media_data['chat_id']},
                {"$set": {"media": media_info}}
            )
    finally:
        await client.disconnect()

async def run_media_consumer():
    await init_mongodb()
    consumer = AIOKafkaConsumer(
        settings.KAFKA_MEDIA_TOPIC,
        bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
        group_id="media_processor_group"
    )
    await consumer.start()
    try:
        async for msg in consumer:
            await process_media(msg)
    finally:
        await consumer.stop()

if __name__ == "__main__":
    asyncio.run(run_media_consumer())