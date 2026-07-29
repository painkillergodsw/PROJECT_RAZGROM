import os
from common.cli_utils.base_config import UtilKafka
from pydantic_settings import SettingsConfigDict, BaseSettings

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.join(BASE_DIR, ".env")


class Kafka(UtilKafka):
    model_config = SettingsConfigDict(env_file=env_path, extra="ignore")

class S3(BaseSettings):
    s3_login: str
    s3_pwd: str
    s3_addr: str

class Config(BaseSettings):
    kafka: Kafka = Kafka()
    s3: S3 = S3()


config = Config()
