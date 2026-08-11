import json
import asyncio
from pathlib import Path
from common.tempfiles import TempListFile, NamedTemporaryFileWDelayedRemove

CUR_DIR = Path(__file__).resolve().parent
BASE_TEMPLATE_PATH = CUR_DIR / "templates" / "base"
binary_path = CUR_DIR / "nuclei"


class SDK:
    async def scan_domains(self, domains: list[str]):
        with TempListFile(domains) as domains_file, \
            NamedTemporaryFileWDelayedRemove(delete=False, suffix=".jsonl") as result_file:

            process = await asyncio.create_subprocess_exec(
                binary_path,
                "-l",
                domains_file,
                "-silent",
                "-j",
                "-o", result_file.name,
                "-t", BASE_TEMPLATE_PATH,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )

            stdout, stderr = await process.communicate()
            stdout = stdout.decode()
            stderr = stderr.decode()

            if process.returncode != 0:
                print(f"Ошибка сканирования доменов {domains}: {stderr}\n {stdout}")
                return {}

            with open(result_file.name, encoding="utf-8") as f:
                return self.__prepare_result(f.read())


    @staticmethod
    def __prepare_result(util_out: str) -> list[dict]:

        if not util_out:
            return []

        result = []

        for line in util_out.splitlines():
            if not line:
                continue

            item = json.loads(line)
            info = item.get("info", {})

            result.append({
                "host": item.get("host"),
                "template": item.get("template"),
                "descr": info.get("description") or info.get("name"),
                "severity": info.get("severity"),
                "tags": info.get("tags", []),
                "extracted-results": item.get("extracted-results")
            })

        return result
