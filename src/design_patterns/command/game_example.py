from typing import List

from src.design_patterns.command.supplement import BaseUnit, Command, MovementDirection


class LandUnit(BaseUnit):
    def move(self, direction: MovementDirection, distance: int) -> None:
        print(f"Moving LandUnit {distance} miles {direction.value}!")

    def destroy(self) -> None:
        print("Self-destructing LandUnit!")


class SeaUnit(BaseUnit):
    def move(self, direction: MovementDirection, distance: int) -> None:
        print(f"Moving SeaUnit {distance} miles {direction.value}!")

    def destroy(self) -> None:
        print("Self-destructing SeaUnit!")


class GameEngine:
    def __init__(self) -> None:
        self._command_queue: List[Command] = []
        self._failed_commands: List[Command] = []

    def execute_turn(self) -> None:
        for command in self._command_queue:
            try:
                command.execute()
            except RuntimeError:
                self._failed_commands.append(command)


class MoveCommand(Command):
    def __init__(
        self, receiver: BaseUnit, direction: MovementDirection, distance: int
    ) -> None:
        self._receiver = receiver
        self._direction = direction
        self._distance = distance

    def execute(self) -> None:
        self._receiver.move(self._direction, self._distance)


class DestroyCommand(Command):
    def __init__(self, receiver: BaseUnit) -> None:
        self._receiver = receiver

    def execute(self) -> None:
        self._receiver.destroy()
