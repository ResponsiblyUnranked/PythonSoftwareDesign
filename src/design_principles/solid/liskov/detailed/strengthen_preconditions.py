class Parrot:
    def __init__(self, name: str) -> None:
        self.name = name

    def speak_number(self, number: int) -> str:
        return f"Hey it's me, {self.name}! Your number is {number}"


class FussyParrot(Parrot):
    def speak_number(self, number: int) -> str:
        if number < 0:
            return "I don't deal with negatives! Give me a real number!"
        return f"Hey it's me, {self.name}! Your number is {number}"
