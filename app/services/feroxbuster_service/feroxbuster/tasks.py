from .feroxbuster import SDK

feroxbuster = SDK()

async def scan_domain(domain: str):
    result = await feroxbuster.scan_domain(domain)
    return result