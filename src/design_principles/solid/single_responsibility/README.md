# Single Responsibility Principle

## Structure

| File      | Description |
| ----------- | ----------- |
| [`./example.py`](example.py)      | Code examples containing anti-patterns and patterns.       |
| [`./supplement.py`](supplement.py)     | Additional code to assist in the examples. You don't need to read this to learn the pattern.        |
| [`tests/design_principles/solid/single_responsibility_test.py`](../../../../tests/design_principles/solid/single_responsibility_test.py)   | Unit tests to show code in action.        |

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
    # other code here...
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

With this in mind, let's take a look at the `# best practice` in `example.py`. We first
notice that we define an interface:

```python
class PlayableSoundFormat(Protocol):
    def get_sound_data(self) -> SoundData:
        ...
```

A note about this code: the `(Protocol)` part indicates this class is an interface,
which means it only _describes_ the expected behaviour of any given class, without
actually implementing it. This is why there is a `...` rather than any actual code.
If you want to read more on Python Protocols,
[here is a great article on them.](https://godatadriven.com/blog/protocols-in-python-why-you-need-them/)
You will see a lot more of them throughout this repository, as they are a great tool
for designing flexible software.

Now when we design a speaker class like `BestSoundSpeaker`, by using the
`PlayableSoundFormat` interface, this is how we get the speaker to "not care" about the
audio file type (as mentioned previously):

```python
class BestSoundSpeaker:
    # other code here...
    def play_sound(self, sound: PlayableSoundFormat) -> Optional[SoundData]:
        if self.powered_on:
            return sound.get_sound_data()
        else:
            return None
```

By specifying `PlayableSoundFormat` as the `sound` type, our speaker no longer "cares"
about what type of audio file we send it, as long as it _acts_ like a
`PlayableSoundFormat` type, then it will be happy. And _this_ is what polymorphism is.

In our example, in order for an object to "act" like a `PlayableSoundFormat` it needs
to have a `.get_sound_data()` method which returns a `SoundData` type. If you look at
the unit test `test_can_play_flac_music_from_best_speaker`, we're using a new type
`FLACFile` which will "act" like a `PlayableSoundFormat`.

And so with this new `BestSoundSpeaker` class, we can create as many audio types as we
like, and our speaker will be able to play them as long as they _implement_ the
`PlayableSoundFormat` interface.

For example, a new class for the OGG Vorbis format
could look like the following:

```python
class OGGVorbis:
    ogg_data: bytes

    def __init__(self, data: bytes):
        self.ogg_data = data
    
    def _process_audio(self) -> bytes:
        # do some processing of the data here
        ...
        
    def get_sound_data(self) -> SoundData:
        processed_audio = self._process_audio(self.ogg_data)
        return SoundData(processed_audio)
```

And this new format will work fine with our `BestSoundSpeaker` because it implements
the `.get_sound_data()` method.

## Conclusion

As you can see, with the Single Responsibility principle from the SOLID Principles,
we've been able to restrict our Sound Speaker class to only have one responsibility -
to play the digital `SoundData` that is passed to it. We removed the Speaker's
dependency on various audio file formats, so that it is not concerned by _what kind_
of audio it receives, but is able to play all sound files that adhere to a standard
`PlayableSoundFormat` type.

Hopefully this has been a good insight into how to separate responsibilities and
concerns, and even touch on other good design principles, like using abstractions and
interfaces.

### Additional reading

 - [Another example of Single Responsibility in Python on GitHub](https://github.com/heykarimoff/solid.python/blob/master/1.srp.py)
 - [ArjanCodes on SOLID Principles](https://www.youtube.com/watch?v=pTB30aXS77U)
