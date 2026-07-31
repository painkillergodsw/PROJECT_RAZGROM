import json
import asyncio
from pathlib import Path
from collections import defaultdict
from common.tempfiles import TempListFile

CUR_DIR = Path(__file__).resolve().parent
binary_path = CUR_DIR / "subfinder"


class SDK:
    async def scan_domains(self, domains: list[str]):
        with TempListFile(domains) as domains_file:

            process = await asyncio.create_subprocess_exec(
                binary_path, "-dL", domains_file, "-silent", "-json",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )

            stdout, stderr = await process.communicate()
            stdout = stdout.decode()
            stderr = stderr.decode()

        if process.returncode != 0:
            print(f"Ошибка сканирования доменов {domains}: {stderr}")
            return {}

        return self.__prepare_result(stdout)

    @staticmethod
    def __prepare_result(util_out: str) -> dict:

        if not util_out:
            return {}

        lines = util_out.split("\n")
        result = defaultdict(list)
        for line in lines:
            if not line:
                continue
            line = json.loads(line)

            result[line.get("input")].append(line.get("host"))
        return dict(result)



