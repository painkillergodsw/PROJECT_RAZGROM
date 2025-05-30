from datetime import datetime, timedelta, UTC
from uuid import uuid4

import pytest
from httpx import AsyncClient, ASGITransport

from app.services.auth_service.run import app
from app.services.auth_service.utils import decode, create_token
from app.services.auth_service.config import config

must_have_keys_access = ("sub", "role", "exp", "iat", "type", "jti")
must_have_keys_refresh = ("sub", "exp", "iat", "type", "jti")


@pytest.fixture
async def client(override_db_session):
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://127.0.0.1",
    ) as ac:
        yield ac


### TEST REGISTRATE ###
@pytest.mark.asyncio
@pytest.mark.parametrize(
    "username, password, password1, expected_status",
    [
        ("testusername1", "123456789qwerty", "123456789qwerty", 200),  # Normal
        ("testusername1", "123456789qwerty", "123456789qwerty", 409),  # Дубликат
        (
            "testusername2",
            "123456789qwert",
            "123456789qwer",
            422,
        ),  # Пароли не совпадают
        ("testusername3", "123", "123", 422),  # Пароль не правильный
        ("test", "123456789qwert", "123456789qwert", 422),  # Логин не правильный
    ],
)
async def test_registrate(client, username, password, password1, expected_status):
    response = await client.post(
        "http://127.0.0.1/users/registrate",
        json={
            "username": username,
            "password": password,
            "password1": password1,
        },
    )

    assert response.status_code == expected_status


async def test_registrate_tokens(client):
    response = await client.post(
        "http://127.0.0.1/users/registrate",
        json={
            "username": "test_real_1",
            "password": "test_pwd1",
            "password1": "test_pwd1",
        },
    )

    response_dict = dict(response.json())
    assert response_dict.get("access_token") is not None
    assert response_dict.get("refresh_token") is not None

    access_tkn_payload = decode(response_dict.get("access_token"))
    refresh_tkn_payload = decode(response_dict.get("refresh_token"))

    assert tuple(access_tkn_payload.keys()) == must_have_keys_access
    assert tuple(refresh_tkn_payload.keys()) == must_have_keys_refresh


### TEST REGISTRATE ###


### TEST AUTH ###
@pytest.mark.asyncio
@pytest.mark.parametrize(
    "username, password, expected_status",
    [
        ("testusername1", "123456789qwerty", 200),
        ("usernotexists", "123456789qwerty", 401),
        ("testusername", "123456789qwerty", 401),
        ("testusername1", "123456", 422),
        ("testu", "123456789qwert", 422),
    ],
)
async def test_auth(client, username, password, expected_status):
    response = await client.post(
        "http://127.0.0.1/users/auth",
        json={
            "username": username,
            "password": password,
        },
    )

    assert response.status_code == expected_status


@pytest.mark.asyncio
async def test_auth_tokens(client):
    response = await client.post(
        "http://127.0.0.1/users/auth",
        json={
            "username": "testusername1",
            "password": "123456789qwerty",
        },
    )

    response_dict = dict(response.json())
    assert response_dict.get("access_token") is not None
    assert response_dict.get("refresh_token") is not None

    access_tkn_payload = decode(response_dict.get("access_token"))
    refresh_tkn_payload = decode(response_dict.get("refresh_token"))
    assert tuple(access_tkn_payload.keys()) == must_have_keys_access
    assert tuple(refresh_tkn_payload.keys()) == must_have_keys_refresh


### TEST AUTH ###


now = datetime.now(UTC)
expire = now + timedelta(hours=config.jwt.refresh_token_lifetime_hour)

payload1 = {
    "exp": expire,
    "iat": now,
    "type": "refresh",
    "jti": str(uuid4()),
    "sub": "999",
}

payload2 = {
    "exp": now - timedelta(seconds=60),
    "iat": now,
    "type": "refresh",
    "jti": str(uuid4()),
    "sub": "1",
}

payload3 = {
    "exp": expire,
    "iat": now,
    "type": "access",
    "jti": str(uuid4()),
    "sub": "1",
}

payload4 = {
    "exp": expire,
    "iat": now,
    "type": "refresh",
    "jti": str(uuid4()),
}

payload5 = {
    "exp": expire,
    "iat": now,
    "type": "refresh",
    "sub": "1",
}

token_w_un_ex_user = create_token(
    payload1
)  # попытка рефреша не существующего пользователя
token_expired = create_token(payload2)  # попытка рефреша с истекшим токеном
token_with_wrong_type = create_token(
    payload3
)  # попытка рефреша с неверным типом токена
token_wout_sub = create_token(payload4)  # попытка рефреша без sub
token_wout_jti = create_token(payload5)  # попытка рефреша без jti


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "token, expected_status",
    [
        (token_w_un_ex_user, 404),
        (token_expired, 400),
        (token_with_wrong_type, 400),
        (token_wout_sub, 400),
        (token_wout_jti, 400),
    ],
)
async def test_refresh(client, token, expected_status):
    response = await client.post(
        "http://127.0.0.1/users/refresh",
        json={
            "refresh_token": token,
        },
    )

    assert response.status_code == expected_status


@pytest.mark.asyncio
async def test_refresh_normal(client):
    response = await client.post(
        "http://127.0.0.1/users/registrate",
        json={
            "username": "normal_user_t",
            "password": "123456qwert",
            "password1": "123456qwert",
        },
    )

    response = dict(response.json())
    refresh_token = response["refresh_token"]

    response_refresh = await client.post(
        url="http://127.0.0.1/users/refresh",
        json={
            "refresh_token": refresh_token,
        },
    )

    assert response_refresh.status_code == 200


### TEST REFRESH ###


### TEST LOGOUT ###
refresh_for_test_u_n_exists = create_token(payload1)
payload1["type"] = "access"
payload1["jti"] = str(uuid4())
access_for_test_u_n_exists = create_token(payload1)

normal_refresh_for_test = create_token(payload3)
payload3["type"] = "access"
payload3["jti"] = str(uuid4())
normal_access_for_test = create_token(payload3)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "access, refresh, expected_status",
    [
        (
            access_for_test_u_n_exists,
            refresh_for_test_u_n_exists,
            404,
        ),  # not exists user
        (normal_access_for_test, None, 200),  # only access
        (None, normal_refresh_for_test, 200),  # only refresh
    ],
)
async def test_logout(client, access, refresh, expected_status):
    response = await client.post(
        "http://127.0.0.1/users/logout",
        json={
            "refresh_token": refresh,
            "access_token": access,
        },
    )

    assert response.status_code == expected_status


@pytest.mark.asyncio
async def test_logout_normal(client):
    response = await client.post(
        "http://127.0.0.1/users/registrate",
        json={
            "username": "normal_user_t2",
            "password": "123456qwert",
            "password1": "123456qwert",
        },
    )

    response = dict(response.json())
    refresh_token = response["refresh_token"]
    access_token = response["access_token"]

    response_logout = await client.post(
        url="http://127.0.0.1/users/logout",
        json={
            "refresh_token": refresh_token,
            "access_token": access_token,
        },
    )

    response_refresh = await client.post(
        url="http://127.0.0.1/users/refresh",
        json={
            "refresh_token": refresh_token,
        },
    )

    assert response_refresh.status_code == 409
    assert response_logout.status_code == 200


### TEST LOGOUT ###
