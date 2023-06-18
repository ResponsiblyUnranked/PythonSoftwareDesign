from enum import Enum
from typing import List


class InvalidEmployeeError(ValueError):
    pass


class Department(Enum):
    SALES = "sales"
    HR = "hr"
    MARKETING = "marketing"
    FINANCE = "finance"
    DEVELOPMENT = "development"


class Employee:
    def __init__(
        self,
        name: str,
        age: int,
        department: Department,
        salary: int = 30_000,
        years_worked: int = 0,
    ) -> None:
        self.name = name
        self.age = age
        self.department = department
        self.salary = salary
        self.years_worked = years_worked
        self.previous_bonus_years: List[int] = []

    def save(self) -> None:
        pass
