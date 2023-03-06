from typing import Optional, Protocol
from uuid import UUID

from src.solid.single_responsibility.supplement import MP3File, SoundData


# anti-pattern
class BadSoundSpeaker:
    speaker_id: UUID
    volume: int
    powered_on: bool

    def __init__(self):
        self.powered_on = False

    def power_on(self):
        self.powered_on = True

    def power_off(self):
        self.powered_on = False

    def change_volume(self, new_volume: int):
        self.volume = new_volume

    def play_music(self, music_file: MP3File) -> Optional[SoundData]:
        if self.powered_on:
            return music_file.stream_mp3_data()
        else:
            return None


# better practice
class GoodSoundSpeaker:
    speaker_id: UUID
    volume: int
    powered_on: bool

    def __init__(self):
        self.powered_on = False

    def power_on(self):
        self.powered_on = True

    def power_off(self):
        self.powered_on = False

    def change_volume(self, new_volume: int):
        self.volume = new_volume

    def play_sound(self, sound: SoundData) -> Optional[SoundData]:
        if self.powered_on:
            return sound
        else:
            return None


# best practice
class PlayableSoundFormat(Protocol):
    def get_sound_data(self) -> SoundData:
        ...


class BestSoundSpeaker:
    speaker_id: UUID
    volume: int
    powered_on: bool

    def __init__(self):
        self.powered_on = False

    def power_on(self):
        self.powered_on = True

    def power_off(self):
        self.powered_on = False

    def change_volume(self, new_volume: int):
        self.volume = new_volume

    def play_sound(self, sound: PlayableSoundFormat) -> Optional[SoundData]:
        if self.powered_on:
            return sound.get_sound_data()
        else:
            return None
