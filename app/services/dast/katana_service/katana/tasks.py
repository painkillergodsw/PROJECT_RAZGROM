from .katana import SDK
import logging as l

logger = l.getLogger(__name__)

katana = SDK()

async def scan_domain(domain: str):
    print(f"Katana начало скана: {domain}")
    result = await katana.find_endpoints(domain)
    print(f"Katana скан окончен : {domain}")

    return result
