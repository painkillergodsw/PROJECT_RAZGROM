from .feroxbuster import SDK
import logging as l

logger = l.getLogger(__name__)

feroxbuster = SDK()

async def scan_domain(domain: str):
    logger.info(f"Feroxbuster начало скана: {domain}")
    result = await feroxbuster.scan_domain(domain)
    logger.info(f"Feroxbuster скан окончен : {domain}")

    return result