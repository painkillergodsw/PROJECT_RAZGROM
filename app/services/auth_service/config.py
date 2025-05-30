import os
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = Path(os.path.join(BASE_DIR, "data"))
CERTS_DIR = Path(os.path.join(BASE_DIR, "certs"))

env_path = os.path.join(BASE_DIR, ".env")


class DBSetting(BaseSettings):
    model_config = SettingsConfigDict(env_file=env_path, extra="ignore")
    DB_USER: str
    DB_PWD: str
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str

    @property
    def conn_url(self) -> str:
        # return f"sqlite+aiosqlite:///{DATA_DIR / "db.sqlite3"}"
        return f"mysql+aiomysql://{self.DB_USER}:{self.DB_PWD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


class JWTSetting(BaseSettings):
    private_key_path: Path = CERTS_DIR / "private.pem"
    public_key_path: Path = CERTS_DIR / "public.pem"
    algorithm: str = "RS256"
    access_token_lifetime_minutes: int = 15
    refresh_token_lifetime_hour: int = 24 * 15


class Config(BaseSettings):
    db: DBSetting = DBSetting()
    jwt: JWTSetting = JWTSetting()


config = Config()
