import redis.asyncio as redis
import os
from dotenv import load_dotenv
import json

load_dotenv()

redis_client = redis.from_url(
    os.getenv("REDIS_URL"),
    decode_responses=True
)


async def get_cache(key: str):
    data = await redis_client.get(key)
    return json.loads(data) if data else None


async def set_cache(key: str, value, expire: int = 60):
    await redis_client.set(
        key,
        json.dumps(value, default=str),
        ex=expire
    )

async def invalidate_cache(pattern: str):
    async for key in redis_client.scan_iter(pattern):
        await redis_client.delete(key)
