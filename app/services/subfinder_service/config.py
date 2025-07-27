import os
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.join(BASE_DIR, ".env")




class Kafka(BaseSettings):
    # model_config = SettingsConfigDict(env_file=env_path, extra="ignore")
    address: str = "kafka:9092"
    consume_t: str = "subdomains.task"
    produce_t: str = "subdomains.subfinder.done"
    group_id: str = "subdomain"

class Config(BaseSettings):
    kafka: Kafka = Kafka()


config = Config()
