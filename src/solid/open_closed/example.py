# anti-pattern
class JuniorTeacher:
    name: str

    def __init__(self, name: str):
        self.name = name

    def teach_class(self, subject: str) -> str:
        if subject == "maths":
            return f"{self.name} is teaching algebra!"

        if subject == "science":
            return f"{self.name} is teaching particle physics!"

        return f"{self.name} is freestyling and teaching {subject}!"
