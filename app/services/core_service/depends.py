from redis.asyncio import Redis

from redis_db.dep.depends import get_redis_client
from schemas import AccessTokenInfoSchema, UserSchema
from fastapi import Header, Depends
from utils import check_access_revoked


async def get_access_token_from_request(
    x_jwt_jti: str = Header(..., alias="x-jwt-jti"),
    x_jwt_sub: int = Header(..., alias="x-jwt-sub"),
    x_jwt_role: str = Header(..., alias="x-jwt-role"),
) -> AccessTokenInfoSchema:
    return AccessTokenInfoSchema(jti=x_jwt_jti, sub=x_jwt_sub, role=x_jwt_role)


async def get_user(
    token: AccessTokenInfoSchema = Depends(get_access_token_from_request),
    redis: Redis = Depends(get_redis_client),
) -> UserSchema:
    await check_access_revoked(token.jti, redis)
    return UserSchema(id=token.sub, role=token.role)
