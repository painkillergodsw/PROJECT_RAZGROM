from .subfinder import SDK

subfinder = SDK()

async def scan_domains(domains: list[str]):
    print(f"SUBFINDER: Старт скана [{domains}]")
    result = await subfinder.scan_domains(domains)
    print(f"SUBFINDER: Конец скана [{domains}]")

    return result