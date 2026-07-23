from .feroxbuster import SDK
import logging as l

logger = l.getLogger(__name__)

feroxbuster = SDK()

async def scan_domain(domain: str):
    print(f"Feroxbuster начало скана: {domain}")
    result = await feroxbuster.scan_domain(domain)
    print(f"Feroxbuster скан окончен : {domain}")

    return result