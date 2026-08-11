import json
import asyncio
from pathlib import Path
from common.tempfiles import TempListFile, NamedTemporaryFileWDelayedRemove

CUR_DIR = Path(__file__).resolve().parent
binary_path = CUR_DIR / "httpx"


class SDK:

    async def scan_pages(self, urls: list[str]):
        with NamedTemporaryFileWDelayedRemove(delete=False) as file, \
            TempListFile(urls) as urls_f:
            process = await asyncio.create_subprocess_exec(
                binary_path, "-l", urls_f, "-td", "-title", "-status-code", "-ct",
                "-cl", "-json", "-o", file.name,

                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )

            stdout, stderr = await process.communicate()

            if process.returncode != 0:
                print(f"Ошибка сканирования {urls}: {stderr}")
                return {}
            return self.__prepare_result(file)


    @staticmethod
    def __prepare_result(file) -> dict[str, dict]:
        file.seek(0)

        result = {}

        for line in file:
            if isinstance(line, bytes):
                line = line.decode("utf-8")

            if not line.strip():
                continue

            item = json.loads(line)

            url = item["url"]

            result[url] = {
                "status_code": item.get("status_code"),
                "content_length": item.get("content_length"),
                "content_type": item.get("content_type"),
                "tech": item.get("tech", []),
                "title": item.get("title"),
            }

        return result
