from abc import ABC, abstractmethod
from enum import Enum


class MovementDirection(Enum):
    NORTH = "NORTH"
    EAST = "EAST"
    SOUTH = "SOUTH"
    WEST = "WEST"


class Command(ABC):
    @abstractmethod
    def execute(self) -> None:
        ...


class BaseUnit(ABC):
    @abstractmethod
    def move(self, direction: MovementDirection, distance: int) -> None:
        ...

    @abstractmethod
    def destroy(self) -> None:
        ...
