from fastapi import FastAPI
from app.api.routes import router
from app.config import settings
from app.database.mongodb import init_mongodb
from app.database.redis import init_redis
from app.utils.logging import setup_logging
from app.services.kafka_service import kafka_service

app = FastAPI()

app.include_router(router)

@app.on_event("startup")
async def startup_event():
    setup_logging()
    await init_mongodb()
    await init_redis()
    await kafka_service.start()

@app.on_event("shutdown")
async def shutdown_event():
    await kafka_service.stop()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)