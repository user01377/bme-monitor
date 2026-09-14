import os
import logging
import asyncio
from redis.asyncio import Redis
from redis.exceptions import ConnectionError

logger = logging.getLogger(__name__)

def create_redis():
    # creates redis object for connection
    return Redis(
        host="redis",
        port=6379,
        password=os.environ['REDIS_PASSWORD'],
        socket_timeout=None,
        decode_responses=True
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