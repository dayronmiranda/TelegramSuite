import asyncio
from telethon import TelegramClient
from app.database.mongodb import get_db
from app.utils.logging import logger
from app.services.webhook_service import send_webhook_notification
from app.services.media_service import download_media_batch
from app.config import settings

async def start_extraction(session_data, chat_id, limit, task_id):
    db = get_db()
    client = TelegramClient(session_data["phone"], session_data["api_id"], session_data["api_hash"])
    try:
        await client.start()
        messages = []
        async for message in client.iter_messages(chat_id, limit=limit):
            message_data = {
                "message_id": message.id,
                "chat_id": str(message.chat_id),
                "date": message.date.isoformat(),
                "text": message.text,
            }
            messages.append(message_data)
            
            if len(messages) >= settings.BATCH_SIZE:
                media_info = await download_media_batch(client, messages, settings.MEDIA_DIRECTORY)
                for media in media_info:
                    message_index = next((index for (index, d) in enumerate(messages) if d["message_id"] == media["message_id"]), None)
                    if message_index is not None:
                        messages[message_index]["media"] = media["media"]
                
                await db.messages.insert_many(messages)
                messages.clear()
                await asyncio.sleep(settings.RATE_LIMIT_DELAY)

        if messages:
            media_info = await download_media_batch(client, messages, settings.MEDIA_DIRECTORY)
            for media in media_info:
                message_index = next((index for (index, d) in enumerate(messages) if d["message_id"] == media["message_id"]), None)
                if message_index is not None:
                    messages[message_index]["media"] = media["media"]
            
            await db.messages.insert_many(messages)
        
        await db.tasks.update_one(
            {"_id": task_id},
            {"$set": {"status": "completed", "progress": 100}}
        )
        
        task = await db.tasks.find_one({"_id": task_id})
        if task.get("webhook_url"):
            await send_webhook_notification(task["webhook_url"], {"status": "completed", "task_id": str(task_id)})
    except Exception as e:
        logger.error(f"Error during extraction: {str(e)}")
        await db.tasks.update_one(
            {"_id": task_id},
            {"$set": {"status": "failed", "error": str(e)}}
        )
        task = await db.tasks.find_one({"_id": task_id})
        if task.get("webhook_url"):
            await send_webhook_notification(task["webhook_url"], {"status": "failed", "task_id": str(task_id), "error": str(e)})
    finally:
        await client.disconnect()