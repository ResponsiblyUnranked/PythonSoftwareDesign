from src.type_hints.supplement import Database


# anti-pattern 1
def add_user(user, dob, name):
    database = Database()
    result = database.create_item(user, dob, name)

    return result
