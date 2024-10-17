import asyncio
from aiokafka import AIOKafkaConsumer
import json
from config import settings
from database.mongodb import get_db, init_mongodb

async def process_message(message):
    db = get_db()
    message_data = json.loads(message.value)
    await db.messages.insert_one(message_data)

async def run_message_consumer():
    await init_mongodb()
    consumer = AIOKafkaConsumer(
        settings.KAFKA_MESSAGE_TOPIC,
        bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
        group_id="message_processor_group"
    )
    await consumer.start()
    try:
        async for msg in consumer:
            await process_message(msg)
    finally:
        await consumer.stop()

if __name__ == "__main__":
    asyncio.run(run_message_consumer())