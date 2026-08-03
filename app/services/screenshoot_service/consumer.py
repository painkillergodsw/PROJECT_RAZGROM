from tasks import make_scrn
from config import config
from common.kafka.consumer import base_create_topics, base_consume

async def create_topics():
    await base_create_topics(config)

async def consume(producer):
    await base_consume(producer, config, handle_msg=handle_msg)

async def handle_msg(producer, msg):
    print("msg recived")

    try:
        print(type(msg.value["urls"]))
        result = await make_scrn(msg.value["urls"])
        await producer.send(config.kafka.PRODUCE_T, result, msg.key)

    except Exception as e:
        print(str(e))   