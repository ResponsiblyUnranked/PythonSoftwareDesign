from enum import Enum
from typing import Protocol


class MovementDirection(Enum):
    NORTH = "NORTH"
    EAST = "EAST"
    SOUTH = "SOUTH"
    WEST = "WEST"


class Command(Protocol):
    def execute(self) -> None:
        ...


class BaseUnit(Protocol):
    def move(self, direction: MovementDirection, distance: int) -> None:
        ...

    def destroy(self) -> None:
        ...
