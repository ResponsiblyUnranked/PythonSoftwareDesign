class Game:
    ...


class VideoGame(Game):
    def save(self) -> None:
        ...


class GameRentalStore:
    def rent_game(self, title: str) -> VideoGame:
        return VideoGame()


class IndieGameRentalStore(GameRentalStore):
    def rent_game(self, title: str) -> Game:  # type: ignore[override]
        return Game()
