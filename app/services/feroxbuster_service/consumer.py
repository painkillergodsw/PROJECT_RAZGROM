from feroxbuster.tasks import scan_domain
from config import config
from common.consumer import base_create_topics, base_consume

async def create_topics():
    await base_create_topics(config)

async def consume(producer):
    await base_consume(producer, config, handle_msg=handle_msg)

async def handle_msg(producer, msg):

    try:
        pages = await scan_domain(msg.value["domain"])
        result = {msg.value["domain"]: pages}
        await producer.send(config.kafka.PRODUCE_T, result, msg.key)

    except Exception as e:
        print(str(e))