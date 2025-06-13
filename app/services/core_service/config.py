import os
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
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
        print(
            f"mysql+aiomysql://{self.DB_USER}:{self.DB_PWD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )
        return f"mysql+aiomysql://{self.DB_USER}:{self.DB_PWD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


class RedisSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=env_path, extra="ignore")
    REDIS_PORT: str
    REDIS_HOST: str
    REDIS_DB: int = 0


class Config(BaseSettings):
    db: DBSetting = DBSetting()
    redis: RedisSettings = RedisSettings()


config = Config()
