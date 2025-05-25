import os
from pathlib import Path

from pydantic_settings import BaseSettings

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = Path(os.path.join(BASE_DIR, "data"))
CERTS_DIR = Path(os.path.join(BASE_DIR, "certs"))


class DBSetting(BaseSettings):
    conn_url: str = f"sqlite+aiosqlite:///{DATA_DIR / "db.sqlite3"}"


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
