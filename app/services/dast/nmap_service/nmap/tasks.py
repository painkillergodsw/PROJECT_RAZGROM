from .nmap import SDK

nmap = SDK()

async def scan_ports(domains: list[str]):
    print(f"Скан портов: {domains}")
    result = await nmap.scan_ports(domains)
    print(f"Конец скан портов: {domains}")
    return result

async def scan_services(domain: str, ports: list[int]):
    print(f"Скан сервисов")
    result = await nmap.scan_service(domain, ports)
    print(f"Конец скан сервисов")

    return result