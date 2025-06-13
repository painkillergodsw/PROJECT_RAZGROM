from pydantic import BaseModel


class AccessTokenInfoFromHeaders(BaseModel):
    sub: int
    jti: str
    role: str


class CreateMainDomain(BaseModel): ...


class CreateProject(BaseModel):
    name: str
    main_domain_lst: list[CreateMainDomain]
