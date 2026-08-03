import asyncio

from katana.tasks import scan_domain
from config import config
from common.kafka.consumer import base_create_topics, base_consume

async def create_topics():
    await base_create_topics(config)

async def consume(producer):
    await base_consume(producer, config, handle_msg=handle_msg)

async def handle_msg(producer, msg):

    try:
        domains = msg.value["domains"]

        # result = []
        # sync
        # for domain in domains:
        #     pages = await scan_domain(domain)
        #     scan_result = {domain: pages}
        #     result.append(scan_result)

        results = await asyncio.gather(
            *(scan_domain(domain) for domain in domains)
        )

        payload = [
            {domain: pages}
            for domain, pages in zip(domains, results)
        ]

        await producer.send(config.kafka.PRODUCE_T, payload, msg.key)

    except Exception as e:
        print(str(e))