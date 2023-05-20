import pytest

from src.solid.liskov.detailed.parameter_types import (
    ConsoleGamer,
    Gamer,
    LivingRoom,
    VideoGame,
)


def test_subclass_usage_works_fine() -> None:
    # given
    my_game = VideoGame()
    gamer = Gamer()

    living_room = LivingRoom(gamer, my_game)

    # when
    result = living_room.start_entertainment()

    # then
    assert result


@pytest.mark.xfail(reason="This test demonstrates an anti-pattern.")
def test_liskov_violation_breaks_code_with_superclass() -> None:
    # given
    my_game = VideoGame()
    gamer = ConsoleGamer()

    living_room = LivingRoom(gamer, my_game)

    # when
    result = living_room.start_entertainment()

    # then
    assert result
