# Detailed Liskov Substitution

_(X minute read)_

## Structure

| File      | Description |
| ----------- | ----------- |
| [`strengthen_preconditions.py`](strengthen_preconditions.py)      | Code example containing a pattern and anti-pattern.       |
| [`../tests/strengthen_preconditions_test.py`](../tests/strengthen_preconditions_test.py)   | Unit tests to show code in action.        |

## What are Preconditions?

The preconditions of a method are conditions that must be met in order for a method to
even run without crashing. Sometimes they can be obvious, an `.update_user()` method 
probably requires that the user exists first. But sometimes they are not.

They can often be hard to identify as they are not always explicitly specified in the
code. Perhaps a method requires some certain data to exist in a database.

When we talk about 'strengthening' the preconditions, this is referring to the idea that
we are either adding _more_ conditions that need to be met, or making the current
conditions _more specific_.

As you'll see, this breaks the LSP and stops you from being able to interchange a
subclass with its parent class.

## Conclusion
