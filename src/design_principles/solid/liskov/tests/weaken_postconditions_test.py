import pytest

from src.design_principles.solid.liskov.detailed.weaken_postconditions import (
    BadDatabaseConnection,
    DatabaseConnection,
)


def test_can_create_database_connection() -> None:
    # when
    connection = DatabaseConnection("192.168.0.24:25565")

    # then
    assert isinstance(connection, DatabaseConnection)
    assert not connection.is_open


def test_can_connect_to_database() -> None:
    # given
    connection = DatabaseConnection("192.168.0.24:25565")

    # when
    connection._open()

    # then
    assert connection.is_open


def test_connection_can_be_closed() -> None:
    # given
    connection = DatabaseConnection("192.168.0.24:25565")
    connection._open()

    # when
    connection._close()

    # then
    assert not connection.is_open


def test_connection_is_closed_after_query() -> None:
    # given
    connection = DatabaseConnection("192.168.0.24:25565")

    # when
    result = connection.query("SELECT * FROM my_data;")

    # then
    assert result
    assert not connection.is_open


def test_can_create_bad_database_connection() -> None:
    # when
    connection = BadDatabaseConnection("192.168.0.24:7777")

    # then
    assert isinstance(connection, BadDatabaseConnection)
    assert not connection.is_open


def test_can_connect_to_bad_database() -> None:
    # given
    connection = BadDatabaseConnection("192.168.0.24:7777")

    # when
    connection._open()

    # then
    assert connection.is_open


def test_bad_connection_can_be_closed() -> None:
    # given
    connection = BadDatabaseConnection("192.168.0.24:7777")
    connection._open()

    # when
    connection._close()

    # then
    assert not connection.is_open


@pytest.mark.xfail(reason="This test demonstrates an anti-pattern.", strict=True)
def test_bad_connection_is_closed_after_query() -> None:
    # given
    connection = BadDatabaseConnection("192.168.0.24:7777")

    # when
    result = connection.query("SELECT * FROM my_data;")

    # then
    assert result
    assert not connection.is_open
