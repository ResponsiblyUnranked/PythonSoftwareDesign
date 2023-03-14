# anti-pattern
from typing import Protocol


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


# best practice
class Subject(Protocol):
    def get_lesson_plan(self) -> str:
        ...


class Maths:
    @staticmethod
    def get_lesson_plan() -> str:
        return "algebra"


class Science:
    @staticmethod
    def get_lesson_plan() -> str:
        return "particle physics"


class SeniorTeacher:
    name: str
    subject: Subject

    def __init__(self, name: str, subject: Subject):
        self.name = name
        self.subject = subject

    def teach_class(self) -> str:
        lesson = self.subject.get_lesson_plan()
        return f"{self.name} is teaching {lesson}!"
