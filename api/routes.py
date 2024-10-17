from fastapi import APIRouter
from api import sessions, extractions, tasks

router = APIRouter()

router.include_router(sessions.router, prefix="/sessions", tags=["sessions"])
router.include_router(extractions.router, prefix="/extractions", tags=["extractions"])
router.include_router(tasks.router, prefix="/tasks", tags=["tasks"])

@router.get("/health")
async def health_check():
    # Implement health check logic
    return {"status": "healthy"}