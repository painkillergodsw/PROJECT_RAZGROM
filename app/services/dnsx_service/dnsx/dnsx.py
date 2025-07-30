import os
import subprocess
import tempfile
from pathlib import Path
from collections import defaultdict
import tldextract

CUR_DIR = Path(__file__).resolve().parent
binary_path = CUR_DIR / "dnsx"
wordlist_path = CUR_DIR / "default_lists" / "base.txt"


class SDK:
    async def scan_domains(self, domains: list[str], sub_parts: list[str]=None):
        if not sub_parts:
            sub_parts = self.__get_default_sub_parts(wordlist_path)

        with TempDomainsFile(domains, sub_parts) as domains_file:
            result = subprocess.run(
                [binary_path, "-l", domains_file],
                capture_output=True,
                text=True,
                check=True,
                stdin=subprocess.DEVNULL
            )
        return self.__prepare_result(result.stdout)

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


class TempDomainsFile:
    def __init__(self, domains: list[str], sub_parts: list[str]):
        self.domains = domains
        self.sub_parts = sub_parts

    def __enter__(self):
        with tempfile.NamedTemporaryFile(mode="w", delete=False, encoding="utf-8") as f:
            self.filepath = f.name

            for domain in self.domains:
                for sub_part in self.sub_parts:
                    f.write(f"{sub_part}.{domain}\n")

        return self.filepath

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.filepath and os.path.exists(self.filepath):
            os.remove(self.filepath)
