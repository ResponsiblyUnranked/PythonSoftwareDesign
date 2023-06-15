import pytest

from src.design_principles.solid.liskov.detailed.return_types import (
    Game,
    GameRentalStore,
    IndieGameRentalStore,
    VideoGame,
)


def test_can_instantiate_game() -> None:
    # when
    game = Game()

    # then
    assert isinstance(game, Game)


def test_can_instantiate_videogame() -> None:
    # when
    game = VideoGame()

    # then
    assert isinstance(game, VideoGame)


def test_can_save_game_from_rental_store() -> None:
    # given
    rental_store = GameRentalStore()

    # when
    my_game = rental_store.rent_game("GoldenEye")

    # then
    my_game.save()


@pytest.mark.xfail(reason="This test demonstrates an anti-pattern.")
def test_can_save_game_from_indie_rental_store() -> None:
    # given
    rental_store = IndieGameRentalStore()

    # when
    my_game = rental_store.rent_game("GoldenEye")

    # then
    my_game.save()  # type: ignore[attr-defined]
