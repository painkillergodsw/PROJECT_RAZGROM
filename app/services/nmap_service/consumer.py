from nmap.tasks import scan_ports, scan_services
from config import config
from common.consumer import base_create_topics, base_consume

async def create_topics():
    await base_create_topics(config, topics=[
        config.kafka.CONSUME_PORT_SCAN_T,
        config.kafka.CONSUME_SERVICE_SCAN_T,
        config.kafka.PRODUCE_PORT_SCAN_T,
        config.kafka.PRODUCE_SERVICE_SCAN_T,
    ])

async def consume(producer):

    await base_consume(
        producer, config,
        handle_msg=handle_msg,
        topics=[
            config.kafka.CONSUME_PORT_SCAN_T,
            config.kafka.CONSUME_SERVICE_SCAN_T
        ]
    )

async def handle_msg(producer, msg):

    try:
        
        if msg.topic == config.kafka.CONSUME_PORT_SCAN_T:
            scan_result = await scan_ports(msg.value["domains"])
            await producer.send(config.kafka.PRODUCE_PORT_SCAN_T, scan_result, msg.key)

        elif msg.topic == config.kafka.CONSUME_SERVICE_SCAN_T:
            for asset in msg.value["assets"]:
                domain = asset.get("domain")
                ports = asset.get("ports")
                scan_result  = await scan_services(domain, ports)
                await producer.send(config.kafka.PRODUCE_SERVICE_SCAN_T, scan_result, msg.key)

    except Exception as e:
        print(str(e))