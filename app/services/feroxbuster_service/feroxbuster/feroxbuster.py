import json
import asyncio
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
                "-o", file.name, "--json", "--no-state", "--threads", "150",
            )

            stdout, stderr = await process.communicate()

            if process.returncode != 0:
                print(f"Ошибка сканирования домена {domain}: {stderr}")
                return []
            return self.__prepare_result(file)


    @staticmethod
    def __prepare_result(file, filtered_status=(404, )) -> list[list[str|int]]:
        result = []
        for line in file.readlines():
            if not line: continue

            obj = json.loads(line)

            if obj['type'] == "response":
                if obj['status'] not in filtered_status:
                    result.append([obj['url'], obj["status"]])

        return result

    @staticmethod
    def __get_default_wordlist():
        return wordlist_path
