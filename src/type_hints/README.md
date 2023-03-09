# Type Hints

## Structure

| File                | Description |
| -----------         | ----------- |
| [`./anti_patterns.py`](anti_patterns.py)  | Examples of what **not** to do, or the problematic code that can be fixed by implementing the design principle.       |
| [`./example.py`](example.py)       | Counter-examples to the anti-patterns, of how the code could be written to improve the anti-pattern.        |
| [`./supplement.py`](supplement.py)     | Additional code to assist in the examples. You don't need to read this to learn the pattern.        |
| [`tests/type_hints_test.py`](../../../tests/type_hints_test.py)   | Unit tests to show code in action.        |

## Tutorial

### What are type hints?

Type hints are as the name suggests, labels for variables, arguments, and functions 
which indicate what type they are. 

### How type hints will make your code better

Take a look at the following code:

```python
# don't do this
def add_user(user, dob, name):
    database = Database()
    result = database.create_item(user, dob, name)

    return result
```

and see if you can answer the following questions:

1. What is `dob`?
2. What's the difference between `user` and `name`?
3. What is `result`?

As you can see, the code does not explain _what_ it is actually doing. Sure, we can work
out that it's adding some sort of user to a database, and `dob` is probably a date of
birth.

But what form does `dob` take? It could be `"2022-01-05"`, or `"Jan-5-1997"` or just
`20230218`.

It is this **uncertainty** that slows down your ability to code quickly and efficiently.
It's when you're trying to:

- fix a bug
- understand your code from 6 months ago
- explain your code to a new team member
- start working on a new project written by somebody else

that you will start to see how this "guesswork" of working out what code does, is not
enough to gain a full understanding and work efficiently.

Take a look at this improved example:

```python
def add_user(user: UUID, dob: datetime.date, name: str) -> User:
    database = Database()
    result = database.create_item(user, dob, name)

    return result
```

You can now easily answer the previous questions:
1. `dob` is a Python `date` object, and likely a date of birth.
2. `user` is a unique ID, whereas `name` is probably first name of the user.
3. `result` is a `User` object, which is dataclass containing information about the
user.

However, this can still be improved further as we are still using words like "likely"
and "probably" in our answers to these questions; there is still guesswork going on.

Using type hints and **descriptive** variable names will make the code even more
readable:

```python
def add_user(user_id: UUID, date_of_birth: datetime.date, username: str) -> User:
    database = Database()
    user = database.create_item(user_id, date_of_birth, username)

    return user
```

### Type hint syntax

Type hints generally follow the syntax of the variable name, followed by a colon (`:`), a
space and then the type hint. For function return types, a hyphen (`-`) and
"greater than" sign (`>`) go after the arguments, but before the colon.

Type hints can be specified in several places:

```python
# at variable declaration
my_age = 25 # before
my_age: int = 25 # after


# in function arguments
def combine_names(a, b): # before
def combine_names(a: str, b: str): # after


# in function returns
def combine_names(a, b): # before
def combine_names(a, b) -> str: # after
```

You can even specify the types of data structures like dictionaries by importing them
from the `typing` standard library:

```python
from typing import Dict, List

some_words: List[str] = ["Hello", "World!"]
some_data = Dict[str, bool] = {"tutorial_complete": True}
```

The square brackets `[ ]` can be used to describe the types _within_ these data
structures. So `Dict[str, bool]` indicates the dictionary has keys made up of `str`
(string) and the values are a `bool` (boolean) type.

## Conclusion

Type hints are an essential way of making your code more readable. Even if you only
work on your own solo projects, it will make them a lot easier to understand when you
come back to them a few months later!

### Additional reading

 - [Real Python article on type checking.](https://realpython.com/python-type-checking/)
 - [Official Python Documentation](https://docs.python.org/3/library/typing.html)