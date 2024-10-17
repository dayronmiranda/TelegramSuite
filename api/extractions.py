from fastapi import APIRouter, HTTPException, BackgroundTasks, Depends
from app.services.extraction_service import start_extraction
from app.database.mongodb import get_db
from app.config import settings
from fastapi_limiter import Limiter
from fastapi_limiter.depends import RateLimiter

router = APIRouter()
limiter = Limiter(key_func=lambda: "global")

@router.post("/")
@limiter.limit(f"{settings.API_RATE_LIMIT}/minute")
async def create_extraction(
    session_id: str,
    chat_id: str,
    limit: int = 100,
    background_tasks: BackgroundTasks,
    db = Depends(get_db),
    rate_limiter: RateLimiter = Depends()
):
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
@limiter.limit(f"{settings.API_RATE_LIMIT}/minute")
async def get_messages(
    chat_id: str,
    page: int = 1,
    page_size: int = 50,
    db = Depends(get_db),
    rate_limiter: RateLimiter = Depends()
):
    skip = (page - 1) * page_size
    messages = await db.messages.find({"chat_id": chat_id}).skip(skip).limit(page_size).to_list(length=page_size)
    total_messages = await db.messages.count_documents({"chat_id": chat_id})
    return {
        "messages": messages,
        "page": page,
        "page_size": page_size,
        "total_messages": total_messages
    }