# Detailed Liskov Substitution

_(3 minute read)_

## Structure

| File      | Description |
| ----------- | ----------- |
| [`parameter_types.py`](parameter_types.py)      | Code example containing an anti-pattern.       |
| [`../tests/parameter_types_test.py`](../tests/parameter_types_test.py)   | Unit tests to show code in action.        |

## Parameter Types

When inheriting from a class, all method parameter types should match, or be _more_
abstract than the superclass (parent) type.

Put simply, if `B()` inherits from `A()` and `A()` has a `.do_something(some_parameter)`
where `some_parameter` is of type `C()`. Then if `B()` overrides `A.do_something(some_parameter)`,
it should not make the type of `some_parameter` more specific than
type `C()`. It can only be `C()`, or a parent class of `C()`.

Yeah, that didn't make it clearer for me either - so let's take a look at the example.
Rather than walk through the full code in the usual order, I will present the code
in an order which helps highlight the problem first.

### The problem

Let's say we have a class, `LivingRoom` which looks like the following:

```python
class LivingRoom:
    def __init__(self, gamer: Gamer, video_game: VideoGame):
        self.gamer = gamer
        self.video_game = video_game

    def start_entertainment(self) -> bool:
        result = self.gamer.play_games(self.video_game)
        return result
```

And our `Gamer` looks like the following (take note of the `game` parameter type):

```python
class Gamer:
    def play_games(self, game: VideoGame) -> bool:
        return True
```

Now let's take a look at a simple test which passes:

```python
def test_subclass_usage_works_fine() -> None:
    # given
    my_game = VideoGame()
    gamer = Gamer()

    living_room = LivingRoom(gamer, my_game)

    # when
    result = living_room.start_entertainment()

    # then
    assert result
```

This test works fine because all the types match up, so we are using the class
as intended.

But what about this test? It fails for some reason:

```python
@pytest.mark.xfail(reason="This test demonstrates an anti-pattern.")
def test_liskov_violation_breaks_code_with_superclass() -> None:
    # given
    my_game = VideoGame()
    gamer = ConsoleGamer()

    living_room = LivingRoom(gamer, my_game)

    # when
    result = living_room.start_entertainment()

    # then
    assert result
```

All we did was change `Gamer` to `ConsoleGamer`. And if we take a (high-level) look at
`ConsoleGamer` we can see that it's a subclass of `Gamer`:

```python
class ConsoleGamer(Gamer):
    ...
```

We are making the following assumption: the `LivingRoom` constructor 
tells us that we can accept any gamer of type `Gamer`, and since `ConsoleGamer` 
inherits from `Gamer`, it is a valid subtype, so it should work right?

This is a _correct_ assumption and interpretation of the code from the type hints. So
why didn't it work?

Well, if we had followed the LSP properly, it _would_ have 
worked. But when we take a closer look at the implementation of `ConsoleGamer`:

```python
# anti-pattern
class ConsoleGamer(Gamer):
    def play_games(self, game: ConsoleGame) -> bool:  # type: ignore[override]
        if game.supported_console != "xbox":
            raise ValueError("Game only supported on xbox.")
        else:
            return True
```

We can see that the signature of `.play_games(...)` has changed! It takes a `game`
parameter of type `ConsoleGame`, a subclass of `VideoGame`:

```python
class ConsoleGame(VideoGame):
    supported_console: str
```

Compare that with the original `.play_games(...)` method of a `Gamer`:

```python
class Gamer:
    def play_games(self, game: VideoGame) -> bool:
        return True
```

And we can see it takes a `game` parameter of type `VideoGame`.

The violation of the LSP occurred when `ConsoleGamer` 
changed the type of the`game` parameter in `.play_games(...)` from `VideoGame` to 
`ConsoleGame`.

Because of this violation, although we'd expect that second test to work, it doesn't
because the more specific parameter type `ConsoleGame` makes use of a property
`supported_console` which doesn't exist in the more generic `VideoGame`.

### The solution

Preventing this issue is simple. In our example, the `ConsoleGamer` should not have
changed the `game: VideoGame` parameter to the more specific `game: ConsoleGame` type.

This is what we mean by:

>...all method parameter types should match, or be _more_
>abstract than the superclass (parent) type.

If we kept the parameter as `game: VideoGame` it would have been fine. It is also
acceptable to make the type _more_ abstract. So in our case, we could have changed the
parameter to `game: Game` since this is the parent class of `VideoGame`:

```python
class Game:
    name: str


class VideoGame(Game):
    ...
```

### Notes

You may have noticed in the definition of the `ConsoleGamer` a comment with:

`# type: ignore[override]`

This is to tell `mypy`, a tool designed to look for
issues with the type-hints in your code, to ignore the error in my code.

[`mypy`](https://mypy.readthedocs.io/en/stable/) is sophisticated enough that it can 
actually detect this violation of the LSP, so I have to use a comment to suppress the warning so
that the project will still pass linting checks in GitHub Actions.