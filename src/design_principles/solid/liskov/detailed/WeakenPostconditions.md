# Detailed Liskov Substitution

_(2 minute read)_

## Structure

| File      | Description |
| ----------- | ----------- |
| [`weaken_postconditions.py`](weaken_postconditions.py)      | Code example containing a pattern and anti-pattern.       |
| [`../tests/weaken_postconditions_test.py`](../tests/weaken_postconditions_test.py)   | Unit tests to show code in action.        |

## What are Post-conditions?

If you've read the article on [avoiding strengthening the pre-conditions](StrengthenPreconditions.md)
(highly recommended) then this topic will be pretty easy to grasp.

The aforementioned article shows us that increasing the number of 'conditions' that need
to be met before running a method in a subclass breaks the LSP. This is the opposite
concept. In the same way that a pebble in a lake creates ripples and an explosion might
leave debris around, our methods can leave their own 'debris' as it were.

The idea of 'weakening' our post-conditions is the idea of adding more 'debris' lying
around after a method has run. It's messy and could create problems that we would not
have had we not have substituted the class for a subclass. That is to say if you
swap a class for a subclass and the subclass leaves more 'debris' lying around than the
original class then you have 'weakened' the post-conditions.

Let's get out of metaphor land and take a look at this idea in action. As with all the
examples in this repository, I recommend you clone this project yourself and experiment
with the code to see how it behaves. Even better would be to write your own examples
to demonstrate the principles.

## The Example

First let us look at the best-practice example:

```python
class DatabaseConnection:
    def __init__(self, hostname: str) -> None:
        self.hostname = hostname
        self.is_open = False

    def _open(self) -> None:
        print(f"Connecting to `{self.hostname}`")
        self.is_open = True
        return

    def _close(self) -> None:
        self.is_open = False
        print("Disconnected.")
        return

    def query(self, query_string: str) -> List[Dict]:
        self._open()
        print(f"Running query `{query_string}`")

        data = [
            {"name": "Ron", "age": 53},
            {"name": "Sokka", "age": 16},
        ]

        self._close()
        return data
```

This is a really plain class for connecting to some imaginary database. To keep things
short and simple I haven't added any actual code for connecting or querying a database.

The most important thing to note is that when we make a query, we are making sure to
close the connection (disconnect) with the database. This is because
(at least historically) it is considered bad-practice to leave your connections to a
database open once you have performed all the operations you need to.

And this can be reflected in our final test for the good database connection:

```python
def test_connection_is_closed_after_query() -> None:
    # given
    connection = DatabaseConnection("192.168.0.24:25565")

    # when
    result = connection.query("SELECT * FROM my_data;")

    # then
    assert result
    assert not connection.is_open
```

where we assert that the connection is closed after our query. But if we try writing
the same test but using our `BadDatabaseConnection` we will see that it fails:

```python
    def test_bad_connection_is_closed_after_query() -> None:
        # given
        connection = BadDatabaseConnection("192.168.0.24:7777")
    
        # when
        result = connection.query("SELECT * FROM my_data;")
    
        # then
        assert result
>       assert not connection.is_open
E       assert not True
E        +  where True = <src.design_principles.solid.liskov.detailed.weaken_postconditions.BadDatabaseConnection object at 0x10fe4ee10>.is_open
```

And this is because of the subtle difference in the query method:

```python
class BadDatabaseConnection(DatabaseConnection):
    def query(self, query_string: str) -> List[Dict]:
        self._open()
        print(f"Running query `{query_string}`")

        data = [
            {"name": "Zuko", "age": 17},
            {"name": "Azula", "age": 18},
        ]

        return data
```

Our `BadDatabaseConnection` does not close the connection after making the query.
**And _this_ is the 'debris' that I was talking about.** Leaving this connection open
is adding more mess and debris to the parent method. It's added unexpected side effects
to this method.

### Why is this a problem?

In our example, we could imagine that our simple database only allows 1 open connection
at a time. The 'debris' we've added in this subclass will cause problems when we try
making a second query - it will fail because it will not be able to open a new
connection since the old one will still be open.

In reality databases can have hundreds or thousands of concurrent connections - but the
principle still applies. If this code was running on all your customers' computers, then
very quickly you'd run out of spare connections!

## Conclusion

Much like its cousin 'strengthening pre-conditions', weakening the post-conditions can
often be something hard to notice if you do not have a good grasp on the codebase at
hand.

Imagine you are new to a project, and there is a lot of code. You could easily miss a
single line that closes the database connection, and then you don't end up adding it
into your subclass.

You'll start noticing a theme here which is that side effects can be _very_ difficult to
keep track of if they are not explicit in your code. This is why good testing,
documentation, and comments go a long way to mainting a clean and bug-free codebase.
