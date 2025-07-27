import json
import logging as l
from aiokafka import AIOKafkaProducer
from config import config

class BaseProducer:
    def __init__(self):
        self.producer = None

    @staticmethod
    def value_serializer(msg):
        return json.dumps(msg).encode("utf-8")

    @staticmethod
    def key_serializer(key):
        if key is None:
            return None
        return str(key).encode("utf-8")  # любое значение → строка → байты

    async def start(self):
        self.producer = AIOKafkaProducer(
            bootstrap_servers=config.kafka.address,
            value_serializer=self.value_serializer,
            key_serializer=self.key_serializer
        )
        await self.producer.start()
        l.info("Kafka Producer started")

    async def stop(self):
        if self.producer:
            await self.producer.flush()
            await self.producer.stop()
            l.info("Kafka Producer stopped")

    async def send(self, topic: str, value, key=None):
        if not self.producer:
            raise RuntimeError("Producer is not started")
        try:
            await self.producer.send(topic=topic, key=key, value=value)
        except Exception as e:
            l.error(f"[Kafka] Error sending message: {e}")
