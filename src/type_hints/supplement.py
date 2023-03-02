from dataclasses import dataclass


@dataclass
class User:
    ...


class Database:
    def create_item(self, *args, **kwargs) -> User:
        ...
