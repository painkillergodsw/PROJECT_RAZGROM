import os
from pydantic_settings import SettingsConfigDict, BaseSettings

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.join(BASE_DIR, ".env")


class Kafka(BaseSettings):
    model_config = SettingsConfigDict(env_file=env_path, extra="ignore")
    CONSUME_PORT_SCAN_T: str
    CONSUME_SERVICE_SCAN_T: str
    PRODUCE_PORT_SCAN_T: str
    PRODUCE_SERVICE_SCAN_T: str
    GROUP_ID: str
    ADDRESS: str

class Config(BaseSettings):
    kafka: Kafka = Kafka()


config = Config()
