from dataclasses import dataclass


@dataclass
class SoundData:
    sound_data: bytes


class MP3File:
    mp3_data: bytes

    def __init__(self, data: bytes):
        self.mp3_data = data

    def stream_mp3_data(self) -> SoundData:
        return SoundData(self.mp3_data)


class WAVFile:
    wav_data: bytes

    def __init__(self, data: bytes):
        self.wav_data = data

    def stream_wav_data(self) -> SoundData:
        return SoundData(self.wav_data)


class FLACFile:
    flac_data: bytes

    def __init__(self, data: bytes):
        self.flac_data = data

    def get_sound_data(self) -> SoundData:
        return SoundData(self.flac_data)
