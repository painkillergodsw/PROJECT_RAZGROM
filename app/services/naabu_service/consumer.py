from naabu.tasks import scan_ports
from config import config
from common.consumer import base_create_topics, base_consume

async def create_topics():
    await base_create_topics(config)

async def consume(producer):
    await base_consume(producer, config, handle_msg=handle_msg)

async def handle_msg(producer, msg):

    try:
        host_ports = await scan_ports(msg.value["assets"])
        result = host_ports
        await producer.send(config.kafka.PRODUCE_T, result, msg.key)

    except Exception as e:
        print(str(e))