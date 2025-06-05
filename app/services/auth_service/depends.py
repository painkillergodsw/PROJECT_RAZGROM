from fastapi import Depends, Body, Header
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession
from HTTPExceptions import (
    UnAuthException,
    UserNotExistsException,
    UserAlreadyLogout,
)
from exceptions import UserAlreadyLogoutException

from redis_db.dep.depends import get_redis_client
from schemas import (
    LoginUser,
    UserSchema,
    TokenPayloadSchema,
    RefreshTokenSchema,
    AccessTokenInfoFromHeaders,
)
from models import User
from utils import check_password, check_access_revoked
from db.dep.depends import get_session
from schemas import LogOutSchema
from utils import try_validate_refresh, try_validate_access


async def get_tokens_for_logout(
    tokens: LogOutSchema = Body(),
    session: AsyncSession = Depends(get_session),
    redis_session: Redis = Depends(get_redis_client),
) -> TokenPayloadSchema:

    access_token_payload = await try_validate_access(
        tokens.access_token, session, redis_session
    )
    refresh_token_payload = await try_validate_refresh(tokens.refresh_token, session)

    if refresh_token_payload is None and access_token_payload is None:
        raise UserAlreadyLogout

    return TokenPayloadSchema(
        refresh_token_payload=refresh_token_payload,
        access_token_payload=access_token_payload,
    )


async def get_access_token_from_request(
    x_jwt_jti: str = Header(..., alias="x-jwt-jti"),
    x_jwt_sub: int = Header(..., alias="x-jwt-sub"),
    x_jwt_role: str = Header(..., alias="x-jwt-role"),
) -> AccessTokenInfoFromHeaders:
    return AccessTokenInfoFromHeaders(jti=x_jwt_jti, sub=x_jwt_sub, role=x_jwt_role)


async def get_user_from_request(
    access_token_info: AccessTokenInfoFromHeaders = Depends(
        get_access_token_from_request
    ),
    session: AsyncSession = Depends(get_session),
    redis_session: Redis = Depends(get_redis_client),
):
    try:
        await check_access_revoked(access_token_info.jti, redis_session)
    except UserAlreadyLogoutException:
        raise UserAlreadyLogout

    user_id = access_token_info.sub
    user_mngr = User.manager(session)
    user = await user_mngr.get_one_or_none({"id": user_id})
    if not user:
        raise UserNotExistsException

    return UserSchema(username=user.username, id=user.id, role=user.role)


async def get_user_from_refresh(
    refresh_token: RefreshTokenSchema = Body(),
    session: AsyncSession = Depends(get_session),
):

    payload_af_validate = await try_validate_refresh(
        refresh_token.refresh_token, session
    )

    if not payload_af_validate:
        raise UserAlreadyLogout

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
