from src.design_patterns.specification.example import Employee
from src.design_patterns.specification.supplement import Department

valid_new_employees = [
    ("Roy", 31, Department.DEVELOPMENT),
    ("Jen", 28, Department.HR),
    ("Moss", 30, Department.FINANCE),
]

invalid_new_employees = [
    ("Jaon", 10, Department.DEVELOPMENT),
    ("Clare", 28, Department.SALES),
    ("Sarah", 102, Department.MARKETING),
    ("", 45, Department.HR),
]

employees_getting_a_raise = [
    Employee("Iroh", 70, Department.SALES, salary=25_000),
    Employee("Azula", 25, Department.SALES, salary=32_000),
]

employees_not_getting_a_raise = [
    Employee("Momo", 12, Department.HR),
    Employee("Zuko", 22, Department.SALES, salary=8_000),
    Employee("Roku", 98, Department.SALES, salary=32_000),
]
