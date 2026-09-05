import os
import logging
import asyncio
from fastapi import Request
from redis.asyncio import Redis
from redis.exceptions import ConnectionError

logger = logging.getLogger(__name__)

def create_redis():
    # creates redis object for connection
    return Redis(
        host="redis",
        port=6379,
        password=os.environ['REDIS_PASSWORD']
    )

async def connect_redis():
    # connects to redis container with retry logic
    redis = create_redis()

    for i in range(1, 6):
        try:
            logger.info("Attempting connection to Redis...")
            await redis.ping()
            logger.info("Redis connected.")
            return redis

        except ConnectionError:
            delay = i * 2

            logger.error(
                "Redis connection error, retrying in %s seconds",
                delay,
            )

            await asyncio.sleep(delay)

    await redis.aclose()
    raise RuntimeError("Redis connection failed.")

def get_redis(request: Request):
    redis = getattr(request.app.state, "redis", None)

    if not redis:
        raise RuntimeError("Redis is not initalized.")
    
    return redis