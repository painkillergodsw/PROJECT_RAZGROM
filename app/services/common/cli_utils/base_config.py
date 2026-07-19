from pydantic_settings import BaseSettings

class UtilKafka(BaseSettings):
    ADDRESS: str
    CONSUME_T: str
    PRODUCE_T: str
    GROUP_ID: str
