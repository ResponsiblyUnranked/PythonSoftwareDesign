from abc import ABC, abstractmethod
from typing import Dict


class PhotoshopToolSelector:
    def brush(self) -> None:
        print("Selecting Brush tool!")

    def eraser(self) -> None:
        print("Selecting Eraser tool!")


class Command(ABC):
    @abstractmethod
    def execute(self) -> None:
        pass


class SelectBrush(Command):
    def __init__(self, receiver: PhotoshopToolSelector):
        self._receiver = receiver

    def execute(self) -> None:
        self._receiver.brush()


class SelectEraser(Command):
    def __init__(self, receiver: PhotoshopToolSelector):
        self._receiver = receiver

    def execute(self) -> None:
        self._receiver.eraser()


class NullCommand(Command):
    def execute(self) -> None:
        pass


class KeyboardHandler:
    def __init__(self, key_bindings: Dict[str, Command]) -> None:
        self._key_bindings = key_bindings

    def handle_input(self, key_pressed: str) -> None:
        command = self._key_bindings.get(key_pressed, NullCommand())
        command.execute()
