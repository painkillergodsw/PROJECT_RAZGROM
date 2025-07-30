from .dnsx import SDK

dnsx = SDK()

async def scan_domains(domains: list[str]):
    result = await dnsx.scan_domains(domains)
    return result