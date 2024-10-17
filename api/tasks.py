from fastapi import APIRouter, HTTPException
from database.mongodb import get_db

router = APIRouter()

@router.get("/{task_id}")
async def get_task_status(task_id: str):
    db = get_db()
    task = await db.tasks.find_one({"_id": task_id})
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return {
        "task_id": str(task["_id"]),
        "status": task["status"],
        "progress": task["progress"]
    }

@router.post("/{task_id}/webhook")
async def set_webhook(task_id: str, webhook_url: str):
    db = get_db()
    task = await db.tasks.find_one({"_id": task_id})
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    await db.tasks.update_one({"_id": task_id}, {"$set": {"webhook_url": webhook_url}})
    return {"message": "Webhook URL set successfully"}