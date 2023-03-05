# Single Responsibility

## Structure

| File      | Description |
| ----------- | ----------- |
| `example.py`      | Code examples containing anti-patterns and patterns.       |
| `supplement.py`     | Additional code to assist in the examples. You don't need to read this to learn the pattern.        |
| `TUTORIAL.md`       | Information on the design principle, and a commentary of the examples.        |
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

 - To allow it to play different types of music files

If we think about how a speaker _actually_ works, it just receives electrical data and
(probably) doesn't care if the music is WAV or MP3, so let's take a look at the better
practice to see how we could improve this speaker.

## Better Practice

Take a look at `GoodSoundSpeaker` in `example.py`. Notice that we've now changed the
`play_music()` method to `play_sound()` instead, which better reflects how a speaker
works, it turns electrical sound data into mechanical sound waves:

```python
class GoodSoundSpeaker:
    ...
    def play_sound(self, sound: SoundData) -> Optional[SoundData]:
        if self.powered_on:
            return sound
        else:
            return None
```

This also means that it is not dependent on a specific format of audio file. This means
that if new audio formats are created, we can still play them through our speaker
without having to update our speaker code at all!

But take a look at one of our unit tests for this improved speaker:

```python
def test_can_play_wav_music_from_good_speaker() -> None:
    # given
    music_data = b"great music"
    music_file = WAVFile(data=music_data)

    speaker = GoodSoundSpeaker()
    speaker.power_on()

    # when
    raw_sound_data = music_file.stream_wav_data()
    speaker_output = speaker.play_sound(raw_sound_data)

    # then
    assert speaker_output == SoundData(music_data)
```

Notice how we have to extract the raw sound data of the music first, then pass that
data to the speaker? Well, this is an example of where if we introduce a couple more
principles of good software design, we can greatly improve this code even further.

## Best Practice

If we use the principle of **polymorphism** and separate the parts of our code which
vary from the parts which stay the same, this code will be even simpler to work with
and expand on in the future.

### What is polymorphism?

In Object Oriented Programming (OOP), polymorphism is the ability of a program to call
a method of an object without knowing its full type. To explain this in the context of
our example, polymorphism would allow our speaker to "not care" about what kind of
audio format we use, as long as it can be converted to `SoundData`, our speaker will be
happy to use it.

### Polymorphism in our example

So if we have a think, there are two main components to our code:
 - The speaker
 - The audio formats we want to play on our speaker

Ideally, the speaker should stay the same, and the audio formats we play on the speaker
could change. In fact, we definitely want the audio formats to be variable, otherwise
we'd be very limited in the types of audio files we could play on our speaker!

If we analyse the process of playing music on our speaker, we can identify 3 key steps:
 1. We create the audio file with our music.
 2. We extract the raw sound data from this file.
 3. We pass the raw sound data to the speaker to be played out loud.

Given that we know that the speaker will stay the same, but the audio formats will
change, we can see that step 1 could vary between file formats, but steps 2 & 3 will be
consistent.