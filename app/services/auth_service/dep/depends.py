import datetime

from fastapi import Depends, Body
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.auth_service.exeptions import (
    UnAuthException,
    TokenExpiredException,
    UserNotExistsException,
    WrongTokenException,
)
from app.services.auth_service.schemas import (
    LoginUser,
    UserSchema,
    TokenPayloadSchema,
    RefreshTokenSchema,
)
from app.services.auth_service.models import User
from app.services.auth_service.utils import check_password
from app.db.dep.depends import get_session
from app.services.auth_service.utils import decode
from app.services.auth_service.schemas import LogOutSchema
from app.services.auth_service.utils import validate_token


async def get_tokens_for_logout(
    tokens: LogOutSchema = Body(), session: AsyncSession = Depends(get_session)
) -> TokenPayloadSchema:

    access_token_payload = await validate_token(tokens.access_token, session)
    refresh_token_payload = (
        await validate_token(tokens.refresh_token, session)
        if tokens.refresh_token
        else None
    )

    return TokenPayloadSchema(
        refresh_token_payload=refresh_token_payload,
        access_token_payload=access_token_payload,
    )


async def get_user_from_refresh(
    refresh_token: RefreshTokenSchema = Body(),
    session: AsyncSession = Depends(get_session),
):
    payload_af_validate = await validate_token(refresh_token.refresh_token, session)

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
