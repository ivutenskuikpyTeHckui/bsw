from typing import AsyncGenerator

import redis.asyncio as redis

from src.adapters.config import (
    REDIS_DB,
    REDIS_PORT,
    REDIS_PASSWORD,
    REDIS_HOST,
)


REDIS_URL = f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}"


redis_client = redis.Redis.from_url(REDIS_URL, decode_responses=True)


def get_redis_client() -> redis.Redis:
    return redis_client