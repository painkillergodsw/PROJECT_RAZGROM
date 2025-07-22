import contextlib
import os
import subprocess
import tempfile
import json
from pathlib import Path
from collections import defaultdict

CUR_DIR = Path(__file__).resolve().parent
binary_path = CUR_DIR / "subfinder"


class SDK:
    def scan_domains(self, domains: list[str]):
        with TempDomainsFile(domains) as domains_file:
             result = subprocess.run(
                [binary_path, "-dL", domains_file, "-silent", "-json"],
                capture_output=True,
                text=True,
                check=True
            )

        return self.__prepare_result(result.stdout)


    def scan_domain(self, domain: str):

        result = subprocess.run(
            [binary_path, "-d", domain, "-silent", "-json"],
            capture_output=True,
            text=True,
            check=True
        )

        return self.__prepare_result(result.stdout)


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

