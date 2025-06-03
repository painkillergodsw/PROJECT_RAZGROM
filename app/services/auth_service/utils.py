import jwt
from datetime import timezone, UTC
from jwt import ExpiredSignatureError
from passlib.context import CryptContext
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession
from config import config
from datetime import datetime, timedelta
from uuid import uuid4
from HTTPExceptions import (
    TokenExpiredException,
    UserNotExistsException,
    WrongTokenException,
)
from exceptions import UserAlreadyLogoutException
from models import User, JWTBlackList

hasher = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(plain_pwd: str) -> str:
    return hasher.hash(plain_pwd)


def check_password(plain_pwd, hashed_pwd) -> bool:
    return hasher.verify(plain_pwd, hashed_pwd)


def create_access_token(
    payload: dict,
) -> str:

    tech_info = get_tech_info("access")
    payload.update(tech_info)
    encoded = create_token(payload)

    return encoded


def create_token(payload):
    return jwt.encode(
        payload,
        config.jwt.private_key_path.read_text(),
        algorithm=config.jwt.algorithm,
    )


def get_tech_info(t_type: str):
    now = datetime.now(UTC)

    ex = None

    if t_type not in ("refresh", "access"):
        raise AttributeError("Wrong type")

    if t_type == "access":
        ex = now + timedelta(minutes=config.jwt.access_token_lifetime_minutes)
    if t_type == "refresh":
        ex = now + timedelta(hours=config.jwt.refresh_token_lifetime_hours)

    return {"exp": ex, "iat": now, "type": t_type, "jti": str(uuid4())}


def create_refresh_token(payload: dict):

    tech_info = get_tech_info("refresh")
    payload.update(tech_info)
    encoded = create_token(payload)

    return encoded


def decode(token) -> dict:
    try:
        return jwt.decode(
            jwt=token,
            key=config.jwt.public_key_path.read_text(),
            algorithms=[config.jwt.algorithm],
        )
    except ExpiredSignatureError:
        raise TokenExpiredException


async def validate_access_token(
    token: str, session: AsyncSession, redis_session: Redis
) -> dict:
    token_payload = await validate_token_base(token, session)

    if token_payload:
        if token_payload.get("type") == "access":
            exists = await redis_session.get(token_payload.get("jti"))
            if exists:
                raise UserAlreadyLogoutException()

        return token_payload


async def validate_refresh_token(token: str, session: AsyncSession) -> dict:

    token_payload = await validate_token_base(token, session)

    if token_payload:
        if token_payload.get("type") == "refresh":
            jwt_blacklist_mngr = JWTBlackList.manager(session)
            exists = await jwt_blacklist_mngr.get_one_or_none(
                {"jti": token_payload.get("jti")}
            )
            if exists:
                raise UserAlreadyLogoutException()

    return token_payload


async def try_validate_refresh(token: str, session: AsyncSession) -> dict | None:
    if not token:
        return None
    try:
        return await validate_refresh_token(token, session)
    except UserAlreadyLogoutException:
        return None


async def try_validate_access(
    token: str, session: AsyncSession, redis: Redis
) -> dict | None:
    if not token:
        return None
    try:
        return await validate_access_token(token, session, redis)
    except UserAlreadyLogoutException:
        return None


async def validate_token_base(token: str, session: AsyncSession) -> dict:

    payload = decode(token)
    user_id = payload.get("sub")
    exp = payload.get("exp")
    jti = payload.get("jti")
    t = payload.get("type")

    exp_time = datetime.fromtimestamp(int(exp), tz=timezone.utc)

    if not t or not jti or not user_id:
        raise WrongTokenException

    if (not exp) or (exp_time < datetime.now(timezone.utc)):
        raise TokenExpiredException

    user_mngr = User.manager(session)
    user = await user_mngr.get_one_or_none({"id": user_id})

    if not user:
        raise UserNotExistsException

    return payload
