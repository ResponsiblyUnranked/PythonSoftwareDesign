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

Maybe at a first glance, nothing seems wrong here, and the first unit test