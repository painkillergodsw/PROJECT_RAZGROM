from schemas import AccessTokenInfoFromHeaders
from fastapi import Header


async def get_access_token_from_request(
    x_jwt_jti: str = Header(..., alias="x-jwt-jti"),
    x_jwt_sub: int = Header(..., alias="x-jwt-sub"),
    x_jwt_role: str = Header(..., alias="x-jwt-role"),
) -> AccessTokenInfoFromHeaders:
    return AccessTokenInfoFromHeaders(jti=x_jwt_jti, sub=x_jwt_sub, role=x_jwt_role)
