import asyncio
import os
from logger import logger as l
from pathlib import Path
import pytest
from app.services.auth_service.run import app
from sqlalchemy.ext.asyncio import (
    async_sessionmaker,
    create_async_engine,
    AsyncSession,
)

from app.db.base import Base
from db.dep.depends import get_session
from app.services.auth_service.models import Role

BASE_DIR = Path(os.path.dirname(os.path.abspath(__file__)))
TEST_DB_FILE = f'{BASE_DIR / "test_db.sqlite3"}'


test_engine = create_async_engine(url=f"sqlite+aiosqlite:///{TEST_DB_FILE}")
async_session_maker = async_sessionmaker(
    test_engine, class_=AsyncSession, expire_on_commit=False
)


async def create_base_role(session: AsyncSession):
    l.info("Создание базовой роли")
    role_mngr = Role.manager(session)
    base_role = await role_mngr.get_one_or_none({"name": "user"})
    if not base_role:
        await role_mngr.add({"name": "user"})


@pytest.fixture(scope="session", autouse=True)
async def setup_db():
    l.info("Создание тестовой базы данных")
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    async with async_session_maker() as session:
        await create_base_role(session)

    yield

    await test_engine.dispose()
    l.info("Удаление тестовой базы данных")

    try:
        os.remove(TEST_DB_FILE)
    except Exception as e:
        l.info(f"При удаление тестовой базы данных произошла ошибка {e}")


@pytest.fixture(scope="session", autouse=True)
async def override_db_session():
    async def override_get_session() -> AsyncSession:
        async with async_session_maker() as session:
            yield session

    app.dependency_overrides[get_session] = override_get_session
    yield
