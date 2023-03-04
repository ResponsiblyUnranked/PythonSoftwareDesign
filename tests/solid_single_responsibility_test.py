import pytest

from src.solid.single_responsibility.example import BadSoundSpeaker
from src.solid.single_responsibility.supplement import MP3File, Sound, WAVFile


def test_can_instantiate_bad_speaker() -> None:
    # when
    speaker = BadSoundSpeaker()

    # then
    assert isinstance(speaker, BadSoundSpeaker)
    assert not speaker.powered_on


def test_can_power_on_bad_speaker() -> None:
    # given
    speaker = BadSoundSpeaker()

    # when
    speaker.power_on()

    # then
    assert speaker.powered_on


def test_can_instantiate_mp3_music_file() -> None:
    # when
    music_file = MP3File(data=b"great music")

    # then
    assert isinstance(music_file, MP3File)


def test_can_play_mp3_music_from_bad_speaker() -> None:
    # given
    music_data = b"great music"
    music_file = MP3File(data=music_data)

    speaker = BadSoundSpeaker()
    speaker.power_on()

    # when
    speaker_output = speaker.play_music(music_file)

    # then
    assert speaker_output == Sound(music_data)


def test_cannot_play_wav_music_from_bad_speaker() -> None:
    # given
    music_data = b"great music"
    music_file = WAVFile(data=music_data)

    speaker = BadSoundSpeaker()
    speaker.power_on()

    # then
    with pytest.raises(AttributeError):
        # when
        speaker.play_music(music_file)  # type: ignore


def test_can_instantiate_sound() -> None:
    # when
    music_data = b"music data"
    sound = Sound(music_data)

    # then
    assert isinstance(sound, Sound)
