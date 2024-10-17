import os
from pydantic import BaseSettings

class Settings(BaseSettings):
    MONGO_URI: str = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
    REDIS_HOST: str = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT: int = int(os.getenv("REDIS_PORT", 6379))
    REDIS_DB: int = int(os.getenv("REDIS_DB", 0))
    MEDIA_DIRECTORY: str = "media"
    LOG_FILE: str = "logs/app.log"
    
    # Nuevas variables de configuración
    BATCH_SIZE: int = int(os.getenv("BATCH_SIZE", 100))
    RATE_LIMIT_DELAY: float = float(os.getenv("RATE_LIMIT_DELAY", 1.0))
    MAX_RETRIES: int = int(os.getenv("MAX_RETRIES", 3))
    WEBHOOK_TIMEOUT: int = int(os.getenv("WEBHOOK_TIMEOUT", 10))
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "DEBUG")
    SESSION_EXPIRY: int = int(os.getenv("SESSION_EXPIRY", 3600))  # 1 hora por defecto
    MEDIA_FILE_SIZE_LIMIT: int = int(os.getenv("MEDIA_FILE_SIZE_LIMIT", 20 * 1024 * 1024))  # 20 MB por defecto
    EXTRACTION_CONCURRENCY: int = int(os.getenv("EXTRACTION_CONCURRENCY", 5))
    REDIS_CACHE_EXPIRY: int = int(os.getenv("REDIS_CACHE_EXPIRY", 300))  # 5 minutos por defecto
    DB_CONNECTION_TIMEOUT: int = int(os.getenv("DB_CONNECTION_TIMEOUT", 5000))  # 5 segundos por defecto
    API_RATE_LIMIT: int = int(os.getenv("API_RATE_LIMIT", 100))  # 100 solicitudes por minuto por defecto
    SCHEDULER_MAX_INSTANCES: int = int(os.getenv("SCHEDULER_MAX_INSTANCES", 10))
    FILE_HASH_ALGORITHM: str = os.getenv("FILE_HASH_ALGORITHM", "md5")
    TEMP_FILE_CLEANUP_INTERVAL: int = int(os.getenv("TEMP_FILE_CLEANUP_INTERVAL", 3600))  # 1 hora por defecto

    class Config:
        env_file = ".env"

settings = Settings()