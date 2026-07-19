import asyncio
import json
from json import JSONDecodeError
from aiokafka import AIOKafkaConsumer
from aiokafka.admin import AIOKafkaAdminClient, NewTopic

class BaseConsumer(AIOKafkaConsumer):
    def __init__(self, topic, config):
        super().__init__(
            topic,
            bootstrap_servers=config.kafka.ADDRESS,
            value_deserializer=self.deserializer,
            key_deserializer=self.deserializer,
            max_poll_interval_ms=30*60*1000
        )

        self.config = config

    @staticmethod
    def deserializer(message):
        try:
            return json.loads(message.decode("utf-8"))
        except JSONDecodeError:
            if isinstance(message, bytes):  
                return message.decode("utf-8")
            else:
                return message

async def base_consume(producer, config, handle_msg: callable):
    consumer = BaseConsumer(config.kafka.CONSUME_T, config)
    await consumer.start()
    try:
        async for msg in consumer:
            asyncio.create_task(handle_msg(producer, msg))
    except Exception as e:
        print(e)
    finally:
        await consumer.stop()


async def base_create_topics(config):
    admin_client = AIOKafkaAdminClient(bootstrap_servers=config.kafka.ADDRESS)
    await admin_client.start()

    try:
        existing_topics = await admin_client.list_topics()
        topics_name = [config.kafka.CONSUME_T, config.kafka.PRODUCE_T]
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


