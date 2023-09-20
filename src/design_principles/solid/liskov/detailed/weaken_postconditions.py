from typing import Dict, List


class DatabaseConnection:
    def __init__(self, hostname: str) -> None:
        self.hostname = hostname
        self.is_open = False

    def _open(self) -> None:
        print(f"Connecting to `{self.hostname}`")
        self.is_open = True
        return

    def _close(self) -> None:
        self.is_open = False
        print("Disconnected.")
        return

    def query(self, query_string: str) -> List[Dict]:
        self._open()
        print(f"Running query `{query_string}`")

        data = [
            {"name": "Ron", "age": 53},
            {"name": "Sokka", "age": 16},
        ]

        self._close()
        return data
