# api/extractions.py
from fastapi import APIRouter, HTTPException, BackgroundTasks, Depends
from services.extraction_service import start_extraction
from database.mongodb import get_db
from config import settings
import time

router = APIRouter()

# Diccionario para rastrear las solicitudes
request_counts = {}
request_limit = settings.API_RATE_LIMIT  # Número máximo de solicitudes permitidas
request_window = 60  # Ventana de tiempo en segundos

async def check_rate_limit(client_id: str):
    current_time = time.time()
    # Limpiar las entradas antiguas
    if client_id in request_counts:
        request_counts[client_id] = [
            timestamp for timestamp in request_counts[client_id] if current_time - timestamp < request_window
        ]
    else:
        request_counts[client_id] = []

    # Verificar si se ha alcanzado el límite
    if len(request_counts[client_id]) >= request_limit:
        return False  # Límite alcanzado

    # Registrar la nueva solicitud
    request_counts[client_id].append(current_time)
    return True  # Solicitud permitida

@router.post("/")
async def create_extraction(
    session_id: str,
    chat_id: str,
    background_tasks: BackgroundTasks,
    limit: int = 100,
    db = Depends(get_db),
    client_id: str = "default_client"  # Cambia esto según tu lógica para identificar clientes
):
    if not await check_rate_limit(client_id):
        raise HTTPException(status_code=429, detail="Rate limit exceeded.")

    session_data = await db.sessions.find_one({"_id": session_id})
    if not session_data:
        raise HTTPException(status_code=404, detail="Session not found.")
    
    task_document = {
        "session_id": session_id,
        "chat_id": chat_id,
        "status": "running",
        "progress": 0,
    }
    task_id = await db.tasks.insert_one(task_document)

    background_tasks.add_task(start_extraction, session_data, chat_id, limit, task_id.inserted_id)
    return {"message": "Extraction started", "task_id": str(task_id.inserted_id)}

@router.get("/{chat_id}")
async def get_messages(
    chat_id: str,
    page: int = 1,
    page_size: int = 50,
    db = Depends(get_db),
    client_id: str = "default_client"  # Cambia esto según tu lógica para identificar clientes
):
    if not await check_rate_limit(client_id):
        raise HTTPException(status_code=429, detail="Rate limit exceeded.")

    skip = (page - 1) * page_size
    messages = await db.messages.find({"chat_id": chat_id}).skip(skip).limit(page_size).to_list(length=page_size)
    total_messages = await db.messages.count_documents({"chat_id": chat_id})
    return {
        "messages": messages,
        "page": page,
        "page_size": page_size,
        "total_messages": total_messages
    }