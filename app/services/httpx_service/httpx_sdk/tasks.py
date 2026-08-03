from .httpx import SDK

httpx = SDK()

async def scan_pages(urls: list[str]):
    print(f"Старт [{urls}]")
    result = await httpx.scan_pages(urls)
    print(f"Конец [{urls}]")

    return result