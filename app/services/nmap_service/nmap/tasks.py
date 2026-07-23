from .nmap import SDK

nmap = SDK()

async def scan_ports(domains: list[str]):
    result = await nmap.scan_ports(domains)
    return result

async def scan_services(domain: str, ports: list[int]):
    result = await nmap.scan_service(domain, ports)
    return result