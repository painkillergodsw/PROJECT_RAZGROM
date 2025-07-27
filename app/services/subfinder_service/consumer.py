import json
import logging as l
from json import JSONDecodeError
from aiokafka import AIOKafkaConsumer
from aiokafka.admin import AIOKafkaAdminClient, NewTopic
from subfinder.tasks import scan_domains
from config import config

class BaseConsumer(AIOKafkaConsumer):
    def __init__(self, topic):
        super().__init__(
            topic,
            bootstrap_servers=config.kafka.address,
            value_deserializer=self.deserializer,
            key_deserializer=self.deserializer
        )

    @staticmethod
    def deserializer(message):
        try:
            return json.loads(message.decode("utf-8"))
        except JSONDecodeError:
            if isinstance(message, bytes):
                return message.decode("utf-8")
            else:
                return message

async def consume(producer):
    consumer = BaseConsumer(config.kafka.consume_t)
    await consumer.start()
    try:
        async for msg in consumer:
            subdomains = await scan_domains(msg.value["domains"])
            await producer.send(config.kafka.produce_t, subdomains, msg.key)
    finally:
        await consumer.stop()


async def create_topics():
    admin_client = AIOKafkaAdminClient(bootstrap_servers=config.kafka.address)
    await admin_client.start()

    try:
        existing_topics = await admin_client.list_topics()
        topics_name = [config.kafka.consume_t, config.kafka.produce_t]
        topics_to_create = []
        for topic_name in topics_name:
            if topic_name not in existing_topics:
                topics_to_create.append(
                    NewTopic(
                    name=topic_name,
                    num_partitions=1,
                    replication_factor=1
                    )
                )

        await admin_client.create_topics(topics_to_create)

    finally:
        await admin_client.close()


