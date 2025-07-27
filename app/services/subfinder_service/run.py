import asyncio
from contextlib import asynccontextmanager
from consumer import consume, create_topics
from producer import BaseProducer
import uvicorn
from fastapi import FastAPI
from views import router

@asynccontextmanager
async def lifespan(app: FastAPI):
    producer = BaseProducer()
    await create_topics()
    await producer.start()
    task = asyncio.create_task(consume(producer))
    yield

    task.cancel()
    await producer.stop()
    try:
        await task
    except asyncio.CancelledError:
        pass

app = FastAPI(lifespan=lifespan)
app.include_router(router)

if __name__ == "__main__":
    uvicorn.run("run:app", port=8230, host="0.0.0.0", reload=True)