# Detailed Liskov Substitution

## Structure

| File      | Description |
| ----------- | ----------- |
| [`./return_types.py`](return_types.py)      | Code example containing an anti-pattern.       |
| [`tests/design_principles/solid/liskov_detailed/return_types_test.py`](../../../../../tests/design_principles/solid/liskov_detailed/return_types_test.py)   | Unit tests to show code in action.        |

## Return Types

When inheriting from a class, all method return types should match, or be _more_
specific than the superclass (parent) method return type.

This is opposite to the [parameter types](ParameterTypes.md) section. In that section
we learnt that the subclass method must have arguments that match, or are more abstract
than the superclass. But here, we learn that the subclass method should have a return
type that matches, or is more specific than the superclass.

### The Problem

### The Solution

### Notes
