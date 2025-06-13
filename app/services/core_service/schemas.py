from pydantic import BaseModel


class AccessTokenInfoSchema(BaseModel):
    sub: int
    jti: str
    role: str


class UserSchema(BaseModel):
    id: int
    role: str


class CreateMainDomain(BaseModel): ...


class CreateProject(BaseModel):
    name: str
    main_domain_lst: list[CreateMainDomain]
