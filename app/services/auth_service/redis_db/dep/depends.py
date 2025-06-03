from config import config
import redis.asyncio as redis


async def get_redis_client() -> redis.Redis:
    client = redis.Redis(
        host=config.redis.REDIS_HOST,
        port=config.redis.REDIS_PORT,
        db=config.redis.REDIS_DB,
    )
    try:
        yield client
    finally:
        await client.close()
