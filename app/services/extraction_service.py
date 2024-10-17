from app.database.mongodb import get_db
from app.utils.logging import logger
from app.services.webhook_service import send_webhook_notification
from app.config import settings
from app.services.kafka_service import kafka_service
from telethon import TelegramClient

async def start_extraction(session_data, chat_id, limit, task_id):
    db = get_db()
    client = TelegramClient(session_data["phone"], session_data["api_id"], session_data["api_hash"])
    try:
        await client.start()
        async for message in client.iter_messages(chat_id, limit=limit):
            message_data = {
                "message_id": message.id,
                "chat_id": str(message.chat_id),
                "date": message.date.isoformat(),
                "text": message.text,
                "session_data": session_data,
                "task_id": str(task_id)
            }
            
            # Enviar el mensaje a Kafka
            await kafka_service.send_message(settings.KAFKA_MESSAGE_TOPIC, message_data)

            if message.media:
                media_task = {
                    "message_id": message.id,
                    "chat_id": str(message.chat_id),
                    "media_id": message.media.id,
                    "session_data": session_data,
                    "task_id": str(task_id)
                }
                await kafka_service.send_message(settings.KAFKA_MEDIA_TOPIC, media_task)

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