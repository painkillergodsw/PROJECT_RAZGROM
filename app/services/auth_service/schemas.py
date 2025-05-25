from typing import Optional

from pydantic import BaseModel, Field, ValidationError, model_validator
from app.services.auth_service.utils import get_password_hash


class CreateUser(BaseModel):
    username: str = Field(min_length=6, max_length=14, description="Имя пользователя")
    password: str = Field(min_length=8, max_length=24, description="Пароль")
    password1: str = Field(
        min_length=8, max_length=24, description="Повторите пароль", exclude=True
    )

    @model_validator(mode="after")
    def validate_password(self, value):
        if not self.password == self.password1:
            raise ValueError("Пароли не совпадают")
        self.password = get_password_hash(self.password)
        return self


class LoginUser(BaseModel):
    username: str = Field(min_length=6, max_length=14, description="Имя пользователя")
    password: str = Field(min_length=8, max_length=24, description="Пароль")


class TokensSchema(BaseModel):
    access_token: str
    refresh_token: str = None


class AccessTokenSchema(BaseModel):
    access_token: str


class RefreshTokenSchema(BaseModel):
    refresh_token: str


class RoleSchema(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class UserSchema(BaseModel):
    id: int
    username: str
    role: RoleSchema

    class Config:
        from_attributes = True


class LogOutSchema(BaseModel):
    access_token: str
    refresh_token: Optional[str] = None


class TokenPayloadSchema(BaseModel):
    access_token_payload: dict
    refresh_token_payload: Optional[dict] = None


class ResponseSchema(BaseModel):
    result: str
