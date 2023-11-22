# The Command Pattern

_(8 minute read)_

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

Maybe we are writing some software like Photoshop! And different keys will activate
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

The `NullCommand` allows us to safely ignore keys which do not have bindings:

```python
class KeyboardHandler:
    def __init__(self, key_bindings: Dict[str, Command]) -> None:
        self._key_bindings = key_bindings

    def handle_input(self, key_pressed: str) -> None:
        command = self._key_bindings.get(key_pressed, NullCommand())
        command.execute()
```

You could just as easily replace this `NullCommand` with a command to raise an error, or
create a popup asking to create a key binding.

By using the command pattern, we could also expand on the example by keeping a history
of every command triggered. We could extend the `KeyboardHandler` to additionally
send any invoked commands to some form of storage in memory, allowing us to keep a log -
and therefore give way to implementing 'undo' functionality.

## Strategy Game Scenario

The previous example shows us how we can be flexible with our code when using the
command pattern - we can trigger the same application code from different areas in
a standardised and controllable manner.

The following example shows us another great feature of using the command pattern:
the ability to schedule or queue commands.

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

#### Side note

_Something important to note is that we provide any dependencies of the command client
code at the point of instantiating the command itself. So when we want to move a unit,
we will also need to provide the details of the direction and distance that we will move
it. As you can see, we provide these as arguments to the command at the point of
instantiating it, **not when we execute it.** This is crucial because as previously
mentioned, we want to be able to pass commands around without worrying about the 
dependencies. So if a command object contains all the dependencies already, that allows
us to execute it whenever we want._

_Given that this is the case, it is worth mentioning that if these dependencies are
conditional, or could change between command creation and command execution, then it
may not be wise to use the command pattern._

We can observe the passing of dependencies for the move command in our example:

```python
class MoveCommand(Command):
    def __init__(
        self, receiver: BaseUnit, direction: MovementDirection, distance: int
    ) -> None:
        self._receiver = receiver
        self._direction = direction
        self._distance = distance

    def execute(self) -> None:
        self._receiver.move(self._direction, self._distance)
```

If we take a look at our game engine, we have a simple implementation of a queue system.
We can add our different 'actions' for a given turn to the queue, and then execute them
all in one go:

```python
class GameEngine:
    def __init__(self) -> None:
        self._command_queue: List[Command] = []
        self._failed_commands: List[Command] = []

    def queue_commands(self, *args: Command) -> None:
        for command in args:
            self._command_queue.append(command)

    def execute_turn(self) -> None:
        for command in self._command_queue:
            try:
                command.execute()
            except RuntimeError:
                self._failed_commands.append(command)
```

This is best demonstrated when we look at a basic test for how we would set up and use
this code:

```python
def test_player_can_take_turn() -> None:
    # given
    engine = GameEngine()
    land_unit = LandUnit()
    sea_unit = SeaUnit()

    first_move = MoveCommand(land_unit, MovementDirection.NORTH, 2)
    second_move = MoveCommand(land_unit, MovementDirection.EAST, 5)
    third_move = MoveCommand(sea_unit, MovementDirection.SOUTH, 6)
    fourth_move = DestroyCommand(land_unit)

    engine.queue_commands(first_move, second_move, third_move, fourth_move)

    # when
    engine.execute_turn()
```

The game engine can add as many commands to the queue as needed, and then we could have
a system for the player to say they are 'ready' for their turn to be executed, at which
point the engine runs through the queued commands.

Like with the Photoshop example, we could add a command history to keep a log of the
game state, as well as allowing the player to view a replay of the game, turn by turn.
Playing the replay would be as simple as re-rendering the execution of each set of
commands per turn.

## Conclusion

Hopefully the second example demonstrates a different use-case of the Command pattern.
It should become clear how useful it is to separate the code for request creation from
execution. With our game example, the `MoveCommand` could be applied to many
types of unit, making it very versatile.
