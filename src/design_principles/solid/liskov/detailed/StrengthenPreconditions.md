# Detailed Liskov Substitution

_(2 minute read)_

## Structure

| File      | Description |
| ----------- | ----------- |
| [`strengthen_preconditions.py`](strengthen_preconditions.py)      | Code example containing a pattern and anti-pattern.       |
| [`../tests/strengthen_preconditions_test.py`](../tests/strengthen_preconditions_test.py)   | Unit tests to show code in action.        |

## What are Preconditions?

The preconditions of a method are conditions that must be met in order for a method to
run without crashing. Sometimes they can be obvious, a `.get_user()` method 
probably requires that the user exists first, but is not normally the case.

They are often hard to identify as they are not always explicitly specified in the
code. Perhaps a method requires some certain data to exist in a database.

When we talk about 'strengthening' the preconditions, this is referring to the idea that
we are either adding _more_ conditions that need to be met, or making the current
conditions _more specific_. The idea of 'strengthening' them comes from the idea that
code can be coupled, and so what you are 'strengthening' is actually the link between
the code and its preconditions. There is a stronger bond between the two, making it
harder to separate and expand off of.

As you'll see, this breaks the LSP and stops you from being able to interchange a
subclass with its parent class.

## The Example

So take a look at our small example. We have a simple `Parrot` class which can speak
a number:

```python
class Parrot:
    def __init__(self, name: str) -> None:
        self.name = name

    def speak_number(self, number: int) -> str:
        return f"Hey it's me, {self.name}! Your number is {number}"

```

And if we look at the tests, we can see that our parrot Peter, can speak back
any number.

The LSP suggests that we should be able to substitute `Parrot` for a subclass and still
be able to speak back numbers. But you can see there is a test that will
fail because our `FussyParrot` Percy will not accept negative numbers.

This is why it can be hard to spot the strengthening of these preconditions. The
signature of the function is still the same:

```python
def speak_number(self, number: int) -> str:
```

Yet the actual permitted values for the `number: int` argument have changed. This is
another example of how easy it can be to break the LSP.

## Conclusion

Although this is a small example it demonstrates just how easy it is to
break the LSP. A good way of finding where you've broken the LSP is to write some
tests which run through the exact same use-cases but are substituting one class for
another, much like we did in this example. You may need to assert for different 
behaviour from the methods, but they should not fail when you use the same inputs.
