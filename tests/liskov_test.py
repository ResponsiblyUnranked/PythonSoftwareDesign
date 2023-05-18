import pytest

from src.solid.liskov.example import Rectangle, Square, double_shape_size


# Introduction
def test_can_change_rectangle_properties() -> None:
    # given
    shape = Rectangle(0, 0)

    # when
    shape.set_width(1.9)
    shape.set_height(0.5)

    # then
    assert shape.width == 1.9
    assert shape.height == 0.5


@pytest.mark.xfail(reason="This test demonstrates an anti-pattern.")
def test_square_violate_liskov_and_fails() -> None:
    # given
    shape = Square(0, 0)

    # when
    shape.set_width(1.9)
    shape.set_height(0.5)

    # then
    assert shape.width == 1.9
    assert shape.height == 0.5


def test_square_sides_always_have_equal_length() -> None:
    # given
    shape = Square(0, 0)

    # when
    shape.set_width(1.9)

    # then
    assert shape.width == 1.9
    assert shape.height == 1.9


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


@pytest.mark.xfail(reason="This test demonstrates an anti-pattern.")
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
