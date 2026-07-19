import os
from common.cli_utils.base_config import UtilKafka
from pydantic_settings import SettingsConfigDict, BaseSettings

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.join(BASE_DIR, ".env")


class Kafka(UtilKafka):
    model_config = SettingsConfigDict(env_file=env_path, extra="ignore")

class Config(BaseSettings):
    kafka: Kafka = Kafka()


config = Config()
