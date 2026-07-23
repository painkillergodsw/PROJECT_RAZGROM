import asyncio
import os
import tempfile
from pathlib import Path
import xml.etree.ElementTree as ET

CUR_DIR = Path(__file__).resolve().parent
binary_path = CUR_DIR / "nmap"


class SDK:
    async def scan_ports(self, assets: list[str]):
        with TempDomainsFile(assets) as domains_file, \
            TempResultFile() as result_file:

            process = await asyncio.create_subprocess_exec(
                binary_path,
                "-iL",
                domains_file,
                "-p-",
                "-sS",
                "-oX",
                result_file,
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
                return self.__prepare_result(f.read(), self.__prepare_result_scan_ports)
            

    async def scan_service(self, domain: str, ports: list[int]):
        with TempResultFile() as result_file:
            process = await asyncio.create_subprocess_exec(
                binary_path,
                "-Pn",
                "-sV",
                "--version-all",
                "-p",
                ",".join(map(str, ports)),
                "-oX",
                 result_file,
                domain,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )

            stdout, stderr = await process.communicate()
            stdout = stdout.decode()
            stderr = stderr.decode()

            if process.returncode != 0:
                print(f"Ошибка сканирования ассета {domain}:{ports}: {stderr}")
                return {}

            with open(result_file, encoding="utf-8") as f:
                return self.__prepare_result(f.read(), self.__prepare_result_scan_service)

    @staticmethod
    def __prepare_result(util_out: str, prepare_func: callable) -> dict:
        return prepare_func(util_out)

    @staticmethod
    def __prepare_result_scan_ports(xml_data: str) -> list[dict]:
        root = ET.fromstring(xml_data)
        result = []

        for host in root.findall("host"):

            domain = None
            additional_domains = []
            ports = []

            for hostname in host.findall("./hostnames/hostname"):
                name = hostname.attrib["name"]
                htype = hostname.attrib.get("type")

                if htype == "user":
                    domain = name
                else:
                    additional_domains.append(name)

            for port in host.findall("./ports/port"):

                state = port.find("state")

                if state is None:
                    continue

                ports.append({
                    "port": int(port.attrib["portid"]),
                    "status": state.attrib["state"]
                })


            result.append({
                "domain": domain,
                "additional_domains": additional_domains,
                "ports": ports
            })


        return result

    @staticmethod
    def __prepare_result_scan_service(util_out: str) -> dict:
        root = ET.fromstring(util_out)

        result = []

        for host in root.findall("host"):

            hostname = None

            hostnames = host.find("hostnames")
            if hostnames is not None:
                for h in hostnames.findall("hostname"):
                    if h.attrib.get("type") == "user":
                        hostname = h.attrib.get("name")
                        break

            services = []

            ports = host.find("ports")

            if ports is not None:
                for port in ports.findall("port"):

                    service = port.find("service")

                    if service is None:
                        continue

                    item = {
                        "port": int(port.attrib.get("portid")),
                        "service": service.attrib.get("name"),
                        "product": service.attrib.get("product"),
                        "conf": int(service.attrib.get("conf", 0)),
                        "version": str(service.attrib.get("version"))
                    }

                    services.append(item)


            result.append({
                "hostname": hostname,
                "services": services
            })

        return result

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
        fd, self.filepath = tempfile.mkstemp(suffix=".xml")
        os.close(fd)
        return self.filepath

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.filepath and os.path.exists(self.filepath):
            os.remove(self.filepath)

