# The Command Pattern

_(X minute read)_

## Structure

| File      | Description |
| ----------- | ----------- |
| [`photoshop_example.py`](photoshop_example.py)      | An example of the command pattern in use.       |
| [`tests/photoshop_example_test.py`](tests/photoshop_example_test.py)   | Tests to show how the command pattern is used by client code.        |
| [`game_example.py`](game_example.py)      | An second example of the command pattern in use.       |
| [`tests/game_example_test.py`](tests/game_example_test.py)   | Test to show the game code in use.        |
| [`supplement.py`](supplement.py)   | Boilerplate code that supports the examples.        |

## Photoshop Scenario: Context

Let's look at a common scenario. We are writing some software for a program that uses
key-bindings. Perhaps these key bindings trigger functions that can also be accessed
via context menus, or other buttons in the software.

Maybe we are writing some software like Photoshop? And different keys will activate
different tools, but these tools can also be accessed via buttons. How do we create a
clean interface for the accessing of these tools? We use the command pattern.

## A Brief Explanation

The main idea behind the command pattern is that any type of _request_ is encapsulated
as an **object.** Thereby allowing you to pass requests around, store them in a 
database, keep track of their history and even swap them in and out during runtime.

In our example, a request could be _'Change the active tool to the brush tool.'_ or
_'Change the active tool to the eraser tool.'_

These such requests could be triggered from multiple areas like buttons, keyboard
shortcuts, or context menus. They should also be swappable, in the same way that you
can change your keybindings in Photoshop, you should be able to plug and play the
various commands.

_Note that these command classes do not perform the application logic themselves, they
merely act as an instance of a **request** to perform the application logic._

### The Nitty-Gritty

To implement the command pattern you would usually need the following:

- An abstract base class to act as a template for all commands
- A concrete command class which inherits the above ABC
- A 'receiver' for the command which performs the application logic
- An 'invoker' which executes commands

Your application logic can create these command 'requests' and provide the 'receiver'
when doing so. The command objects can then be passed to various 'invokers' which
will execute the command using the included receiver.

## Photoshop Scenario: Using The Command Pattern

If you look at the Photoshop example code, you will see we have followed the above
guidance and defined:

- A `Command` ABC
- Our 'receiver' which can activate various Photoshop tools, `PhotoshopToolSelector`
- Three commands including a `NullCommand`
- Our 'invoker', `KeyboardHandler`

If you look at the tests for this code, you can see how the added complexity to our code
results in a simpler _interface_ for dealing with keyboard bindings. We can now create a
simple key map and feed that into the `KeyboardHandler`:

```python
def test_can_use_commands() -> None:
    # given
    tool_selector = PhotoshopToolSelector()

    key_bindings = {
        "b": SelectBrush(tool_selector),
        "e": SelectEraser(tool_selector),
    }

    key_handler = KeyboardHandler(key_bindings)

    # when
    key_handler.handle_input("b")
    key_handler.handle_input("e")
```

The `NullCommand` allows us to safely ignore keys which do not have bindings.
You could just as easily replace this `NullCommand` with a command to raise an error, or
create a popup asking to create a key binding:

```python
class KeyboardHandler:
    def __init__(self, key_bindings: Dict[str, Command]) -> None:
        self._key_bindings = key_bindings

    def handle_input(self, key_pressed: str) -> None:
        command = self._key_bindings.get(key_pressed, NullCommand())
        command.execute()
```

By using the command pattern, we could also expand on the example by keeping a history
of every command triggered. We could extend the `KeyboardHandler` to additionally
send any invoked commands to some form of storage in memory, allowing us to keep a log -
and therefore give way to implementing 'undo' functionality.

## Strategy Game Scenario

The previous example shows us how we can be flexible with our code when using the
command pattern - we can trigger the same application code from different areas in
a standardised and controllable manner.

The following example shows us another great feature of using the command pattern,
the ability to schedule, or queue commands.

I envisage us building a turn-based strategy game where you can plan several 'actions'
in advance. Each of these 'actions' will be a command. This is where the queueing of
commands reveals itself, as it will allow our player to plan several moves in advance
and then execute them in sequence on their turn.

### The Code

Take a look at the `game_example.py` code. _Note: I've moved some boilerplate code (like
the `Command` ABC) to the `supplement.py` file to keep this example shorter._

Can you identify our receivers and invoker?

We have 2 receivers, a `LandUnit` and a `SeaUnit`. I picture these being controllable
characters in our game. You can move them or destroy them. Our
`GameEngine` is our invoker and handles the player's turn. Finally, we have the
corresponding commands for moving and destroying a unit.
