from pydantic import BaseModel


class AccessTokenInfoSchema(BaseModel):
    sub: int
    jti: str
    role: str


class UserSchema(BaseModel):
    id: int
    role: str


class CreateProject(BaseModel):
    name: str
    main_domains: list[str]


class MainDomainSchema(BaseModel):
    id: int
    domain: str


class ProjectSchema(BaseModel):
    id: int
    name: str
    main_domains: list[MainDomainSchema]
