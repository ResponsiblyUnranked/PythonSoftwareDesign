# anti-pattern
class VideoGame:
    name: str


class PCGame(VideoGame):
    operating_system: str


class Gamer:
    def play_games(self, game: VideoGame) -> bool:
        return True


class PCGamer(Gamer):
    def play_games(self, game: PCGame) -> bool:  # type: ignore[override]
        if game.operating_system != "windows":
            raise ValueError("Games only work on Windows.")
        else:
            return True


class LivingRoom:
    def __init__(self, gamer: Gamer, video_game: VideoGame):
        self.gamer = gamer
        self.video_game = video_game

    def start_entertainment(self) -> bool:
        result = self.gamer.play_games(self.video_game)
        return result
