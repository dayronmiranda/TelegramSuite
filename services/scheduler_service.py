from apscheduler.schedulers.asyncio import AsyncIOScheduler
from app.services.extraction_service import start_extraction
from app.config import settings

scheduler = AsyncIOScheduler(max_instances=settings.SCHEDULER_MAX_INSTANCES)

def init_scheduler():
    scheduler.start()

def schedule_extraction(session_data, chat_id, limit, frequency):
    job = scheduler.add_job(
        start_extraction,
        'interval',
        seconds=frequency,
        args=[session_data, chat_id, limit]
    )
    return job.id

def remove_scheduled_extraction(job_id):
    scheduler.remove_job(job_id)