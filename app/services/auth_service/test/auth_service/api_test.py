import pytest
from httpx import AsyncClient, ASGITransport

from app.services.auth_service.run import app


@pytest.mark.asyncio
async def test_registrate():
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://127.0.0.1",
    ) as ac:
        response = await ac.post(
            "http://127.0.0.1/users/registrate",
            json={
                "username": "pgod.sw.2",
                "password": "290704ilya",
                "password1": "290704ilya",
            },
        )


@pytest.mark.asyncio
async def test_2(): ...
*