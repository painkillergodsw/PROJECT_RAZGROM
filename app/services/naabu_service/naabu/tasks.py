from .naabu import SDK

naabu = SDK()

async def scan_ports(domains: list[str]):
    print(f"Старт [{domains}]")
    result = await naabu.scan_ports(domains)
    print(f"Конец [{domains}]")

    return result