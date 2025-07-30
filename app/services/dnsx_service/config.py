import os
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.join(BASE_DIR, ".env")




class Kafka(BaseSettings):
    model_config = SettingsConfigDict(env_file=env_path, extra="ignore")
    ADDRESS: str
    CONSUME_T: str
    PRODUCE_T: str
    GROUP_ID: str

class Config(BaseSettings):
    kafka: Kafka = Kafka()


config = Config()
