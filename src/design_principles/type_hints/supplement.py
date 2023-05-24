from dataclasses import dataclass
from typing import Any


@dataclass
class User:
    db_details: Any


class Database:
    def create_item(self, *args, **kwargs) -> User:
        return User(self)
