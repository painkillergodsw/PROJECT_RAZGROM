from .dnsx import SDK

dnsx = SDK()

async def scan_domains(domains: list[str]):
    print(f"DNSX: Старт скана [{domains}]")
    result = await dnsx.scan_domains(domains)
    print(f"DNSX: Конец скана [{domains}]")

    return result