from .subfinder import SDK

subfinder = SDK()

async def scan_domains(domains: list[str]):
    result = await subfinder.scan_domains(domains)
    return result