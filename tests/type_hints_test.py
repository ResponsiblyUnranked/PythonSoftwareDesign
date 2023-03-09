import datetime
import uuid

from src.type_hints.example import add_user
from src.type_hints.supplement import User


def test_example_returns_correct_type() -> None:
    # given
    user_id = uuid.uuid4()
    date_of_birth = datetime.date(2000, 1, 1)
    username = "foo"

    # when
    response = add_user(user_id, date_of_birth, username)

    # then
    assert isinstance(response, User)
