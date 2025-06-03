from fastapi import Depends, Body
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession
from HTTPExceptions import (
    UnAuthException,
    UserNotExistsException,
    WrongTokenException,
    UserAlreadyLogout,
)

from exceptions import UserAlreadyLogoutException
from redis_db.dep.depends import get_redis_client
from schemas import (
    LoginUser,
    UserSchema,
    TokenPayloadSchema,
    RefreshTokenSchema,
)
from models import User
from utils import check_password
from db.dep.depends import get_session
from schemas import LogOutSchema
from utils import validate_token


async def try_validate(
    token: str | None, session: AsyncSession, redis_session: Redis
) -> dict | None:
    if not token:
        return None
    try:
        return await validate_token(token, session, redis_session)
    except UserAlreadyLogoutException:
        return None


async def get_tokens_for_logout(
    tokens: LogOutSchema = Body(),
    session: AsyncSession = Depends(get_session),
    redis_session: Redis = Depends(get_redis_client),
) -> TokenPayloadSchema:

    access_token_payload = await try_validate(
        tokens.access_token, session, redis_session
    )
    refresh_token_payload = await try_validate(
        tokens.refresh_token, session, redis_session
    )

    if refresh_token_payload is None and access_token_payload is None:
        raise UserAlreadyLogout

    return TokenPayloadSchema(
        refresh_token_payload=refresh_token_payload,
        access_token_payload=access_token_payload,
    )


async def get_user_from_refresh(
    refresh_token: RefreshTokenSchema = Body(),
    session: AsyncSession = Depends(get_session),
):

    payload_af_validate = await try_validate(refresh_token.refresh_token, session)

    if not payload_af_validate:
        raise UserAlreadyLogout

    if payload_af_validate.get("type") != "refresh":
        raise WrongTokenException

    if payload_af_validate.get("type") != "refresh":
        raise WrongTokenException

    user_id = payload_af_validate.get("sub")
    user_mngr = User.manager(session)
    user = await user_mngr.get_one_or_none({"id": user_id})
    if not user:
        raise UserNotExistsException

    return UserSchema(username=user.username, id=user.id, role=user.role)


async def authenticate(
    auth_data: LoginUser, session: AsyncSession = Depends(get_session)
) -> UserSchema:

    user_mngr = User.manager(session)
    user = await user_mngr.get_one_or_none({"username": auth_data.username})
    if user is None:
        raise UnAuthException

    if not check_password(auth_data.password, user.password):
        raise UnAuthException

    return UserSchema.from_orm(user)
