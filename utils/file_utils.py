import os
import hashlib
from config import settings
from database.mongodb import get_db

async def calculate_file_hash(file_path):
    hash_obj = hashlib.new(settings.FILE_HASH_ALGORITHM)
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_obj.update(chunk)
    return hash_obj.hexdigest()

async def find_existing_file(file_hash):
    db = get_db()
    file_hash_doc = await db.file_hashes.find_one({"hash": file_hash})
    if file_hash_doc:
        file_path = file_hash_doc["file_path"]
        if os.path.isfile(file_path):
            return file_path
        else:
            # Si el archivo ya no existe, eliminar el documento
            await db.file_hashes.delete_one({"hash": file_hash})
    return None

async def save_file_hash(file_path, file_hash):
    db = get_db()
    await db.file_hashes.update_one(
        {"hash": file_hash},
        {"$set": {"file_path": file_path}},
        upsert=True
    )

async def process_media_file(file_path):
    if os.path.getsize(file_path) > settings.MEDIA_FILE_SIZE_LIMIT:
        os.remove(file_path)
        return None

    file_hash = await calculate_file_hash(file_path)
    existing_file = await find_existing_file(file_hash)
    
    if existing_file:
        os.remove(file_path)
        return existing_file
    else:
        await save_file_hash(file_path, file_hash)
        return file_path