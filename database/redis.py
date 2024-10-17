import redis
from config import settings

redis_client = None

def init_redis():
    global redis_client
    redis_client = redis.StrictRedis(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        db=settings.REDIS_DB,
        decode_responses=True
    )

def close_redis():
    if redis_client:
        redis_client.close()

def get_redis():
    return redis_client

def cache_set(key, value, expiry=None):
    expiry = expiry or settings.REDIS_CACHE_EXPIRY
    redis_client.setex(key, expiry, value)

def cache_get(key):
    return redis_client.get(key)