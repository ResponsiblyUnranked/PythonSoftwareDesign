from src.design_patterns.command.game_example import (
    DestroyCommand,
    GameEngine,
    LandUnit,
    MoveCommand,
    SeaUnit,
)
from src.design_patterns.command.supplement import MovementDirection


def test_player_can_take_turn() -> None:
    # given
    engine = GameEngine()
    land_unit = LandUnit()
    sea_unit = SeaUnit()

    first_move = MoveCommand(land_unit, MovementDirection.NORTH, 2)
    second_move = MoveCommand(land_unit, MovementDirection.EAST, 5)
    third_move = MoveCommand(sea_unit, MovementDirection.SOUTH, 6)
    fourth_move = DestroyCommand(land_unit)

    engine.queue_commands(first_move, second_move, third_move, fourth_move)

    # when
    engine.execute_turn()
