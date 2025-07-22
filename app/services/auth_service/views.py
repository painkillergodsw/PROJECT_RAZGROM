from datetime import datetime, timezone
from redis.asyncio import Redis
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from jwcrypto import jwk
from config import config
from redis_db.dep.depends import get_redis_client
from schemas import (
    CreateUser,
    UserSchema,
    TokensSchema,
    TokenPayloadSchema,
    ResponseSchema,
    AccessTokenSchema,
    PubKeySchema,
)

from db.dep.depends import get_session
from models import User
from HTTPExceptions import UserAlreadyExistsHTTPException
from depends import (
    authenticate,
    get_user_from_refresh,
    get_tokens_for_logout,
    get_user_from_request,
)
from models import JWTBlackList
from utils import (
    create_access_token,
    create_refresh_token,
)

router = APIRouter(prefix="/users")


@router.post("/registrate")
async def registrate(
    user_data: CreateUser, session: AsyncSession = Depends(get_session)
) -> TokensSchema:
    user_mngr = User.manager(session)
    exist_user = await user_mngr.get_one_or_none(
        filters={"username": user_data.username}
    )
    if exist_user:
        raise UserAlreadyExistsHTTPException

    user = await user_mngr.add(user_data)
    access_token = create_access_token({"sub": str(user.id), "role": user.role.name})
    refresh_token = create_refresh_token({"sub": str(user.id)})

    return TokensSchema(access_token=access_token, refresh_token=refresh_token)


@router.post("/auth")
def auth(
    user: UserSchema = Depends(authenticate),
) -> TokensSchema:

    access_token = create_access_token({"sub": str(user.id), "role": user.role.name})
    refresh_token = create_refresh_token({"sub": str(user.id)})

    return TokensSchema(access_token=access_token, refresh_token=refresh_token)


@router.post("/refresh")
def refresh(user: UserSchema = Depends(get_user_from_refresh)) -> AccessTokenSchema:
    access_token = create_access_token({"sub": str(user.id)})
    return AccessTokenSchema(access_token=access_token)


@router.post("/logout")
async def logout(
    tokens_payload: TokenPayloadSchema = Depends(get_tokens_for_logout),
    session: AsyncSession = Depends(get_session),
    redis_session: Redis = Depends(get_redis_client),
) -> ResponseSchema:
    jwt_blacklist_mngr = JWTBlackList.manager(session)

    if tokens_payload.access_token_payload:
        ex = datetime.fromtimestamp(
            int(tokens_payload.access_token_payload.get("exp")), tz=timezone.utc
        )

        now = datetime.now(timezone.utc)
        second_left = (ex - now).total_seconds()

        jti = tokens_payload.access_token_payload.get("jti")

        await redis_session.set(jti, "revoke", ex=int(second_left))

    if tokens_payload.refresh_token_payload:
        await jwt_blacklist_mngr.add(
            {
                "jti": tokens_payload.refresh_token_payload.get("jti"),
                "expire_at": datetime.fromtimestamp(
                    int(tokens_payload.refresh_token_payload.get("exp")),
                    tz=timezone.utc,
                ),
            }
        )

    return ResponseSchema(result="Success")


@router.get("/tech/pubkey")
async def pubkey() -> PubKeySchema:
    return PubKeySchema(
        keys=[jwk.JWK.from_pem(config.jwt.public_key_path.read_bytes())]
    )


@router.get("/me")
async def me(user: UserSchema = Depends(get_user_from_request)) -> UserSchema:
    return UserSchema(username=user.username, id=user.id, role=user.role)


@router.get("/health_check")
async def health_check() -> dict:
    return {"status": "ok"}
