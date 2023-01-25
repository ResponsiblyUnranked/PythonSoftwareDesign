# Single Responsibility

## Structure

| File      | Description |
| ----------- | ----------- |
| `example.py`      | Code examples containing anti-patterns and patterns.       |
| `tests/solid_single_responsibility_test.py`   | Unit tests to show code in action.        |

## Anti-pattern

Take a look at `BadSoundSpeaker` in `example.py`. This is a class to manage a speaker.
As you can see, the functions that are available to us seem to make sense for a speaker.
We can:

 - Turn on the speaker with `power_on()`
 - Turn off the speaker with `power_off()`
 - Change the volume with `change_volume()`
 - Play music with `play_music()`

Maybe at a first glance, nothing seems wrong here, and if you look at the unit test
`test_can_play_mp3_music_from_bad_speaker` then you'll see that playing music works just
fine.

But what if we want to play a WAV file instead of an MP3? If we try running the
following test instead:

```python
def test_can_play_wav_music_from_bad_speaker() -> None:
    # given
    music_data = b"great music"
    music_file = WAVFile(data=music_data)

    speaker = BadSoundSpeaker()
    speaker.power_on()

    # when
    speaker_output = speaker.play_music(music_file)

    # then
    assert speaker_output == music_data
```

then the test fails with an exception:

```python
    def play_music(self, music_file: MP3File) -> Optional[bytes]:
        if self.powered_on:
>           return music_file.stream_mp3_data()
E           AttributeError: 'WAVFile' object has no attribute 'stream_mp3_data'
```

And this is where the underlying problem is: we can't play different types of music
through the speaker without modifying the speaker's `play_music()` method.

This is bad because ideally, **classes should only have 1 reason to change.**

In our example, the `BadSoundSpeaker` class might change for more than one reason:

 - To change the speaker mechanics. For example, maybe we need a 'standby' mode instead
of just 'off', or maybe the volume control is now automatic.

 - To allow it to play different types of music

