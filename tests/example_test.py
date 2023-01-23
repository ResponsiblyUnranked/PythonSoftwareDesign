import pytest

from src.example.some_code import add_two_numbers


@pytest.mark.parametrize(
    "x, y, expected_sum",
    [
        (1, 2, 3),
        (2, 2, 4),
        (2, 3, 5),
    ],
)
def test_add_two_numbers(x: int, y: int, expected_sum: int) -> None:
    result = add_two_numbers(x, y)
    assert result == expected_sum
