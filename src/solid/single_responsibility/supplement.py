from dataclasses import dataclass


@dataclass
class Sound:
    sound_data: bytes


class MP3File:
    mp3_data: bytes

    def __init__(self, data: bytes):
        self.mp3_data = data

    def stream_mp3_data(self) -> Sound:
        return Sound(self.mp3_data)


class WAVFile:
    wav_data: bytes

    def __init__(self, data: bytes):
        self.wav_data = data

    def stream_wav_data(self) -> Sound:
        return Sound(self.wav_data)
