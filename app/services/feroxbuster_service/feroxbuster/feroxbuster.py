import json
import asyncio
from collections import defaultdict
from tempfile import NamedTemporaryFile
from pathlib import Path

CUR_DIR = Path(__file__).resolve().parent
binary_path = CUR_DIR / "feroxbuster"
wordlist_path = CUR_DIR / "default_lists" / "base.txt"


class SDK:
    async def scan_domain(self, domain: str, wordlist = None):

        if not wordlist:
            wordlist = self.__get_default_wordlist()

        with NamedTemporaryFile(delete=True) as file:
            process = await asyncio.create_subprocess_exec(
                binary_path, "-u", domain, "-w", wordlist, "-r", "--random-agent",
                "-o", file.name, "--json", "--no-state", "--depth", "10",
                "-x", "php,html,txt,json,xml,js",
                "--threads", "200",
                "--collect-extensions",
                "--collect-words",
                "--collect-backups",
                "--scan-dir-listings",
                "--smart",         

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
            if not line.strip():
                continue

            obj = json.loads(line)

            if obj.get('type') == "response" and obj.get('status') not in filtered_status:
                result[obj['status']].append(obj['url'])

        return dict(result)

    @staticmethod
    def __get_default_wordlist():
        return wordlist_path
