from motor.motor_asyncio import AsyncIOMotorClient
from config import settings

mongo_client = None
db = None

async def init_mongodb():
    global mongo_client, db
    mongo_client = AsyncIOMotorClient(settings.MONGO_URI, serverSelectionTimeoutMS=settings.DB_CONNECTION_TIMEOUT)
    db = mongo_client.telegram_sessions
    
    # Crear índice único para la colección de hashes de archivos
    await db.file_hashes.create_index("hash", unique=True)
    
async def close_mongodb():
    if mongo_client:
        mongo_client.close()

def get_db():
    return db