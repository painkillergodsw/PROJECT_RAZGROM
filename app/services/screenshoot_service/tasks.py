from config import config
from screenshooter import Screenshooter
from common.fsstorage.fsstorage import Storage

storage = Storage(
    addr=config.s3.s3_addr,
    access_key=config.s3.s3_login,
    secret_key=config.s3.s3_pwd,
    buckets=["screenshoots"],
)

async def save_callback(
    object_name: str,
    bytes: bytes
):

    result = await storage.upload_png(
        "screenshoots", object_name=object_name, data=bytes
    )
    return result

scrnshtr = Screenshooter(
    workers=10,
    save_callback=save_callback
)


async def make_scrn(urls: list[str]):
    print(f"Старт сбора скриншотов {urls}")
    print(f"Законченна инициализация скриншотера")
    result = await scrnshtr.capture_many("example_project_id", urls)
    print(f"Скриншоты собраны {urls}")

    return result