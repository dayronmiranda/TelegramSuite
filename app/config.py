import os
from pydantic import BaseSettings

class Settings(BaseSettings):
    # ... (configuraciones existentes)
    
    # Configuraciones de Kafka
    KAFKA_BOOTSTRAP_SERVERS: str = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
    KAFKA_MESSAGE_TOPIC: str = os.getenv("KAFKA_MESSAGE_TOPIC", "telegram-messages")
    KAFKA_MEDIA_TOPIC: str = os.getenv("KAFKA_MEDIA_TOPIC", "telegram-media")
    KAFKA_TASK_TOPIC: str = os.getenv("KAFKA_TASK_TOPIC", "telegram-tasks")

    class Config:
        env_file = ".env"

settings = Settings()