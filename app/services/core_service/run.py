import uvicorn
from fastapi import FastAPI
from contextlib import asynccontextmanager
from config import config
from views import router
import redis.asyncio as redis
from redis.exceptions import ConnectionError
from logger import logger as l


@asynccontextmanager
async def start(app: FastAPI):
    client = redis.Redis(
        host=config.redis.REDIS_HOST,
        port=config.redis.REDIS_PORT,
        db=config.redis.REDIS_DB,
    )
    try:
        pong = await client.ping()
        l.info(f"redis connection: {str(pong)}")
    except ConnectionError:
        l.error("redis connection error")
    yield


app = FastAPI(lifespan=start)
app.include_router(router)

if __name__ == "__main__":
    uvicorn.run("run:app", port=8229, host="0.0.0.0", reload=True)
