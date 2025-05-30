from datetime import timezone, UTC
import jwt
from jwt import ExpiredSignatureError
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.auth_service.config import config
from datetime import datetime, timedelta
from uuid import uuid4
from app.services.auth_service.exeptions import (
    TokenExpiredException,
    UserNotExistsException,
    WrongTokenException,
    UserAlreadyLogoutEx,
)
from app.services.auth_service.models import User
from app.services.auth_service.models import JWTBlackList

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

    if t_type not in ("refresh", "access"):
        raise AttributeError("Wrong type")

    now = datetime.now(UTC)
    expire = now + timedelta(hours=config.jwt.refresh_token_lifetime_hour)

    return {"exp": expire, "iat": now, "type": t_type, "jti": str(uuid4())}


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


async def validate_token(token: str, session: AsyncSession) -> dict:
    """
    Токен должен содержать информацию о существующем пользователе, время жизни и уникальный идентификатор
    так же быть действительным
    """

    print(token)
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

    jwt_blacklist_mngr = JWTBlackList.manager(session)
    exists = await jwt_blacklist_mngr.get_one_or_none({"jti": jti})

    if exists:
        raise UserAlreadyLogoutEx()

    return payload
