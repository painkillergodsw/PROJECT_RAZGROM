from httpx_sdk.tasks import scan_pages
from config import config
from common.kafka.consumer import base_create_topics, base_consume

async def create_topics():
    await base_create_topics(config)

async def consume(producer):
    await base_consume(producer, config, handle_msg=handle_msg)

async def handle_msg(producer, msg):

    try:
        scan_page_result = await scan_pages(msg.value["urls"])
        await producer.send(config.kafka.PRODUCE_T, scan_page_result, msg.key)

    except Exception as e:
        print(str(e))