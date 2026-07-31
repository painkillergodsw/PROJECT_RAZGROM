import os
import tempfile


class TempSubDomainsFile:
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

class TempListFile:
    def __init__(self, list_in: list[str]):
        self.list_in = list_in

    def __enter__(self):
        with tempfile.NamedTemporaryFile(mode="w", delete=False, encoding="utf-8") as f:
            self.filepath = f.name

            for item in self.list_in:
                f.write(f"{item}\n")

        return self.filepath

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.filepath and os.path.exists(self.filepath):
            os.remove(self.filepath)

class NamedTemporaryFileWDelayedRemove:
    def __init__(self, *args, **kwargs):
        self._tmp = tempfile.NamedTemporaryFile(*args, **kwargs)

    def __getattr__(self, name):
        return getattr(self._tmp, name)

    def __iter__(self):
        return iter(self._tmp)

    @property
    def name(self):
        return self._tmp.name

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            self._tmp.close()
        finally:
            if os.path.exists(self.name):
                os.remove(self.name)