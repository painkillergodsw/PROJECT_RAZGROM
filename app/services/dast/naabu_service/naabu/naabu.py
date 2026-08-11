import json
import asyncio
from pathlib import Path
from collections import defaultdict
from tempfile import NamedTemporaryFile
from common.tempfiles import TempListFile

CUR_DIR = Path(__file__).resolve().parent
binary_path = CUR_DIR / "naabu"


class SDK:
    async def scan_ports(self, assets: list[str]):
        with TempListFile(assets) as domains_file, \
            NamedTemporaryFile(delete=True, suffix=".jsonl") as result_file:

            process = await asyncio.create_subprocess_exec(
                binary_path,
                "-list",
                domains_file,
                "-json",
                "-silent",
                "-o", result_file.name,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )

            stdout, stderr = await process.communicate()
            stdout = stdout.decode()
            stderr = stderr.decode()

            if process.returncode != 0:
                print(f"Ошибка сканирования доменов {assets}: {stderr}")
                return {}

            with open(result_file.name, encoding="utf-8") as f:
                return self.__prepare_result(f.read())


    @staticmethod
    def __prepare_result(util_out: str) -> dict:

        if not util_out:
            return {}

        result = defaultdict(list)

        for line in util_out.splitlines():
            if not line:
                continue

            line = json.loads(line)

            host = line.get("host")
            port = line.get("port")

            result[host].append(port)
            
        return {
            host: sorted(ports) for host, ports in result.items()
        }


