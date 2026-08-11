from .nuclei import SDK

nuclei = SDK()

async def scan_domains(domains: list[str]):
    print(f"DAST скан")
    result = await nuclei.scan_domains(domains)
    print(f"Конец DAST скана")

    return result