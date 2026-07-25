import json
import asyncio
from collections import defaultdict
from tempfile import NamedTemporaryFile
from pathlib import Path

CUR_DIR = Path(__file__).resolve().parent
binary_path = CUR_DIR / "katana"


class SDK:

    async def find_endpoints(self, domain: str):
        with NamedTemporaryFile(delete=True) as file:
            process = await asyncio.create_subprocess_exec(
                binary_path, "-u", domain, "-d", "3", "-jc", "-jsl",
                "-xhr-extraction", "-kf", "all", "-retry", "6", "-timeout", "20", "--headless",
                "-jsonl", "-o", file.name,

                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )

            stdout, stderr = await process.communicate()

            if process.returncode != 0:
                print(f"Ошибка сканирования домена {domain}: {stderr}")
                return {}
            return self.__prepare_result(file)


    @staticmethod
    def __prepare_result(file, filtered_status=(404,)) -> dict[int, list[str]]:
        result = defaultdict(list)

        file.seek(0)

        for line in file:
            line = line.strip()
            if not line:
                continue

            try:
                obj = json.loads(line)
            except json.JSONDecodeError:
                continue

            endpoint = obj.get("request", {}).get("endpoint")
            if not endpoint:
                continue

            response = obj.get("response")
            status = response.get("status_code", 0) if response else 0

            if status not in filtered_status:
                result[status].append(endpoint)

        return dict(result)