class MP3File:
    mp3_data: bytes

    def __init__(self, data: bytes):
        self.mp3_data = data

    def stream_mp3_data(self):
        return self.mp3_data


class WAVFile:
    wav_data: bytes

    def __init__(self, data: bytes):
        self.wav_data = data

    def stream_wav_data(self):
        return self.wav_data
