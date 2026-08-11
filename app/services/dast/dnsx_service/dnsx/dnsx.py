import asyncio
import tldextract

from pathlib import Path
from collections import defaultdict
from common.tempfiles import TempSubDomainsFile

CUR_DIR = Path(__file__).resolve().parent
binary_path = CUR_DIR / "dnsx"
wordlist_path = CUR_DIR / "default_lists" / "base.txt"


class SDK:
    async def scan_domains(self, domains: list[str], sub_parts: list[str]=None):
        if not sub_parts:
            sub_parts = self.__get_default_sub_parts(wordlist_path)

        with TempSubDomainsFile(domains, sub_parts) as domains_file:
            process = await asyncio.create_subprocess_exec(
                binary_path, "-l", domains_file,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                stdin=asyncio.subprocess.DEVNULL,
            )

            stdout, stderr = await process.communicate()
            stdout = stdout.decode()
            stderr = stderr.decode()

            if process.returncode != 0:
                print(f"Ошибка сканирования доменов {domains}: {stderr}")
                return {}

        return self.__prepare_result(stdout)

    @staticmethod
    def __get_default_sub_parts(path: Path):
        with open(path, "r") as f:
            lines = f.readlines()
        return [line.strip() for line in lines]

    @staticmethod
    def __prepare_result(util_out: str) -> dict:

        if not util_out:
            return {}

        lines = util_out.split("\n")
        result = defaultdict(list)
        for line in lines:
            if not line:
                continue

            sub_d_info = tldextract.extract(line)
            result[
                f"{sub_d_info.domain}.{sub_d_info.suffix}"
            ].append(f"{sub_d_info.subdomain}.{sub_d_info.domain}.{sub_d_info.suffix}")

        return dict(result)
