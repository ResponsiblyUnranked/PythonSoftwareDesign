from pathlib import Path

import pytest

from src.design_principles.solid.liskov.detailed.exceptions import (
    FileError,
    MacOSFileReader,
    SystemFileReader,
    WindowsFileReader,
)


def test_normal_exceptions_are_caught() -> None:
    # given
    reader = SystemFileReader()

    try:
        # when
        reader.open_file(Path("test.txt"))
    except FileError:
        # then
        assert True


def test_subclass_follows_liskov() -> None:
    # given
    reader = WindowsFileReader()

    try:
        # when
        reader.open_file(Path("test.txt"))
    except FileError:
        # then
        assert True


@pytest.mark.xfail(reason="This test demonstrates an anti-pattern.")
def test_subclass_breaks_liskov() -> None:
    # given
    reader = MacOSFileReader()

    try:
        # when
        reader.open_file(Path("test.txt"))
    except FileError:
        # then
        assert True
