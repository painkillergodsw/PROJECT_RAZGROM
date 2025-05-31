import uvicorn
from fastapi import FastAPI
from views import router
from contextlib import asynccontextmanager
from models import Role
from db.db import async_session_maker


@asynccontextmanager
async def start(app: FastAPI):
    async with async_session_maker() as session:
        role_mngr = Role.manager(session)
        base_role = await role_mngr.get_one_or_none({"name": "user"})

        if not base_role:
            print("Базовая роль не найдена. Создание")
            await role_mngr.add({"name": "user"})

        yield


app = FastAPI(lifespan=start)
app.include_router(router)

if __name__ == "__main__":
    uvicorn.run("run:app", port=9999, reload=True)
