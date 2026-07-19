import asyncio
import os
import tempfile
import json
from pathlib import Path
from collections import defaultdict

CUR_DIR = Path(__file__).resolve().parent
binary_path = CUR_DIR / "naabu"


class SDK:
    async def scan_ports(self, assets: list[str]):
        with TempDomainsFile(assets) as domains_file, \
            TempResultFile() as result_file:

            process = await asyncio.create_subprocess_exec(
                binary_path,
                "-list",
                domains_file,
                "-json",
                "-silent",
                "-o", result_file,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )

            stdout, stderr = await process.communicate()
            stdout = stdout.decode()
            stderr = stderr.decode()

            if process.returncode != 0:
                print(f"Ошибка сканирования доменов {assets}: {stderr}")
                return {}

            with open(result_file, encoding="utf-8") as f:
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


class TempDomainsFile:
    def __init__(self, domains: list[str]):
        self.domains = domains

    def __enter__(self):
        with tempfile.NamedTemporaryFile(mode="w", delete=False, encoding="utf-8") as f:
            self.filepath = f.name

            for domain in self.domains:
                f.write(f"{domain}\n")

        return self.filepath

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.filepath and os.path.exists(self.filepath):
            os.remove(self.filepath)


class TempResultFile:
    def __init__(self):
        self.filepath = None

    def __enter__(self):
        fd, self.filepath = tempfile.mkstemp(suffix=".jsonl")
        os.close(fd)
        return self.filepath

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.filepath and os.path.exists(self.filepath):
            os.remove(self.filepath)

