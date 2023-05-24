class Game:
    name: str


class VideoGame(Game):
    ...


class ConsoleGame(VideoGame):
    supported_console: str


class Gamer:
    def play_games(self, game: VideoGame) -> bool:
        return True


# anti-pattern
class ConsoleGamer(Gamer):
    def play_games(self, game: ConsoleGame) -> bool:  # type: ignore[override]
        if game.supported_console != "xbox":
            raise ValueError("Game only supported on xbox.")
        else:
            return True


class LivingRoom:
    def __init__(self, gamer: Gamer, video_game: VideoGame):
        self.gamer = gamer
        self.video_game = video_game

    def start_entertainment(self) -> bool:
        result = self.gamer.play_games(self.video_game)
        return result
