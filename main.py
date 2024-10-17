from fastapi import FastAPI
from api.routes import router
from config import settings
from database.mongodb import init_mongodb
from database.redis import init_redis
from utils.logging import setup_logging
from services.kafka_service import kafka_service
from redis.asyncio import Redis

app = FastAPI()

app.include_router(router)

async def init_redis():
    redis_client = Redis(host='localhost', port=6379, db=0)
    await redis_client.ping()
    return redis_client

@app.on_event("startup")
async def startup_event():
    setup_logging()
    await init_mongodb()
    await init_redis()
    #await kafka_service.start()

@app.on_event("shutdown")
async def shutdown_event():
    await kafka_service.stop()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)