from src.solid.single_responsibility.example import BadSoundSpeaker


def test_can_instantiate_bad_speaker() -> None:
    speaker = BadSoundSpeaker()
    assert isinstance(speaker, BadSoundSpeaker)

