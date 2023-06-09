class Game:
    ...


class VideoGame(Game):
    def save(self) -> None:
        ...


class CardGame(Game):
    ...


class GameRentalStore:
    def rent_game(self, title: str) -> VideoGame:
        return VideoGame()


class IndieGameRentalStore(GameRentalStore):
    def rent_game(self, title: str) -> Game:  # type: ignore[override]
        return CardGame()
