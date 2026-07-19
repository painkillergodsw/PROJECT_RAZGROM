from .naabu import SDK

naabu = SDK()

async def scan_ports(domains: list[str]):
    result = await naabu.scan_ports(domains)
    return result