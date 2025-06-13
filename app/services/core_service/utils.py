from HTTPExceptions import UserAlreadyLogoutHTTPException
from redis.asyncio import Redis


async def check_access_revoked(jti: str, redis_session: Redis):
    exists = await redis_session.get(jti)
    if exists:
        raise UserAlreadyLogoutHTTPException
    return True
