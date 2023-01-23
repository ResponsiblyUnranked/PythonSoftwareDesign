import datetime
from uuid import UUID

from src.type_hints.supplement import Database, User


# example 1
def add_user(user: UUID, dob: datetime.date, name: str) -> User:
    database = Database()
    result = database.create_item(user, dob, name)

    return result


# example 2
def add_user_2(user_id: UUID, date_of_birth: datetime.date, username: str) -> User:
    database = Database()
    user = database.create_item(user_id, date_of_birth, username)

    return user
