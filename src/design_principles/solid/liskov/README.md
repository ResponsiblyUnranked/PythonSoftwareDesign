# Liskov Substitution

_(4 minute read)_

## Structure

| File      | Description |
| ----------- | ----------- |
| [`example.py`](example.py)      | Code examples containing anti-patterns and patterns.       |
| [`tests/liskov_test.py`](tests/liskov_test.py)   | Unit tests to show code in action.        |
| [`detailed/`](detailed)      | More detailed examples of the Liskov substitution principle.       |

## Introduction

The consequences of following the Liskov substitution principle (LSP) are many. So this guide
will be broken down into an introduction, plus 5 sections to look more closely at
each of these consequences.

So what is the basic premise of the LSP? It's the idea that
subclasses should be able to replace an instance of their superclass without breaking
the code.

_Sorry what?_

If we have a class `Car` and a class `FordFocus` which inherits from `Car`, this means
that `FordFocus` is a subclass of `Car`. And if these classes follow the LSP, then
wherever our code expects a `Car`, it should still work if we provide
it with a `FordFocus` instead.

[Robert C. Martin](https://en.wikipedia.org/wiki/Robert_C._Martin) suggested that
the LSP can sometimes be represented by something that sounds
normal in natural language, but doesn't work when programming.

Perhaps the most common example is the square-rectangle example. In our natural language,
a Square is _technically_ a rectangle as revealed by a simple Google search:

> A square is a shape that has four equal length sides and four 90 degree right angles.
> A rectangle is a shape with four straight sides and four right angles.
> That means that by definition, a square can be classed as a rectangle.

So how could this be a problem when programming? Let's take a look at the violation
in `example.py`.

### Simple Example

If we look at the `Rectangle` and `Square` classes, they make sense in terms of our
natural language representation. The square is a subtype of rectangle and the
methods are slightly different in the sense that changing the width of a square should
automatically update the height also, since they are always the same:

```python
# violation of Liskov
class Rectangle:
    width: float
    height: float

    def set_width(self, value: float) -> None:
        self.width = value

    def set_height(self, value: float) -> None:
        self.height = value


class Square(Rectangle):
    def set_width(self, value: float) -> None:
        self.width = value
        self.height = value

    def set_height(self, value: float) -> None:
        self.height = value
        self.width = value

```

But let's take a look at `tests/liskov_test.py`. While the first test passes fine:

```python
def test_can_change_rectangle_properties() -> None:
    # given
    shape = Rectangle()

    # when
    shape.set_width(1.9)
    shape.set_height(0.5)

    # then
    assert shape.width == 1.9
    assert shape.height == 0.5
```

The problem is that **we cannot substitute the `Rectangle` for the `Square`**:

```python
def test_square_violate_liskov_and_fails() -> None:
    # given
    shape = Square()

    # when
    shape.set_width(1.9)
    shape.set_height(0.5)

    # then
    assert shape.width == 1.9
    assert shape.height == 0.5
```

This test fails because obviously, a square must have a height equal to length.

---

_As a small side note, I will now keep these 'example' fail-tests in the code for you to
view, but will mark them with:_

```python
@pytest.mark.xfail(reason="This test demonstrates an anti-pattern.")
```

_to indicate that they are part of an anti-pattern, and should not pass._

---

Now I know what you're thinking: _why don't we just change the test? It doesn't even make
sense because a square would have equal length sides._ And you'd be right, the following
test makes a lot more sense, doesn't it?

```python
def test_square_sides_always_have_equal_length() -> None:
    # given
    shape = Square()

    # when
    shape.set_width(1.9)

    # then
    assert shape.width == 1.9
    assert shape.height == 1.9
```

And although this works, this doesn't really demonstrate the problem as the test is
now essentially testing just the `Square` class, and doesn't really have anything to
do with `Rectangle` anymore.

The issue really shows when we _expect_ a `Rectangle` but provide a `Square` instead.

So let's look at some code that better highlights the problem with violating the LSP:

```python
def double_shape_size(shape: Rectangle) -> Rectangle:
    shape.set_width(2 * shape.width)
    shape.set_height(2 * shape.height)
    return shape
```

This seems simple enough, we just double the properties of `Rectangle` and return them:

```python
def test_can_double_rectangle_size() -> None:
    # given
    original_width = 3.2
    original_height = 1.0

    shape = Rectangle(original_width, original_height)

    # when
    larger_shape = double_shape_size(shape)

    # assert
    assert larger_shape.width == 2 * original_width
    assert larger_shape.height == 2 * original_height
```

and this test works just fine. But the function says it accepts (and returns) any
`Rectangle` type. Well, by definition in our code, a `Square` **is** a subtype of
`Rectangle`, so let's try using a square instead:

```python
def test_cannot_double_square_size() -> None:
    # given
    original_width = 3.2
    original_height = 1.0

    shape = Square(original_width, original_height)

    # when
    larger_shape = double_shape_size(shape)

    # assert
    assert larger_shape.width == 2 * original_width
    assert larger_shape.height == 2 * original_height
```

This test fails! When we run pytest:

```
============================= test session starts ==============================
collecting ... collected 1 item

liskov_test.py::test_cannot_double_square_size FAILED                    [100%]
liskov_test.py:60 (test_cannot_double_square_size)
12.8 != 6.4

Expected :6.4
Actual   :12.8
<Click to see difference>

def test_cannot_double_square_size() -> None:
        # given
        original_width = 3.2
        original_height = 1.0
    
        shape = Square(original_width, original_height)
    
        # when
        larger_shape = double_shape_size(shape)
    
        # assert
>       assert larger_shape.width == 2 * original_width
E       assert 12.8 == 6.4

liskov_test.py:72: AssertionError


============================== 1 failed in 0.31s ===============================

Process finished with exit code 1
```

And this test fails as a result of not following the LSP. If
a `Square` inherits from `Rectangle` it should act like a `Rectangle` and _extend_ its
behaviour, not modify it. [_Sound familiar?_](../open_closed/README.md)

As we will see later, this is an example of **strengthening the pre-conditions.** Just
one of the many ways that we can violate the LSP!

## Conclusion

As shown in this tutorial, sometimes the LSP is not always
immediately obvious to us as a developer, especially when the inheritance hierarchy
makes sense when talking about objects with natural language.

If you want to dive into this principle more deeply, take a look inside the
[`./detailed`](detailed) directory. It contains the specific rules which form the
basis of the LSP.

### Additional reading

 - [Another example of Liskov substitution in Python on GitHub](https://github.com/heykarimoff/solid.python/blob/master/3.lsp.py)
 - [ArjanCodes on SOLID Principles](https://www.youtube.com/watch?v=pTB30aXS77U)
 