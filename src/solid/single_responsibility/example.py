from typing import Optional
from uuid import UUID

from src.solid.single_responsibility.supplement import MP3File


# anti-pattern
class BadSoundSpeaker:
    speaker_id: UUID
    volume: int
    powered_on: bool

    def power_on(self):
        ...

    def power_off(self):
        ...

    def change_volume(self, new_volume: int):
        ...

    def play_music(self, music_file: MP3File) -> Optional[bytes]:
        if self.powered_on:
            return music_file.stream_mp3_data()
        else:
            return None
