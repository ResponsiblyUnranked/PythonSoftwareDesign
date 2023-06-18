from src.design_patterns.specification.supplement import Department, Employee

valid_new_employees = [
    ("Roy", 31, Department.DEVELOPMENT),
    ("Jen", 28, Department.HR),
    ("Moss", 30, Department.FINANCE),
]

invalid_new_employees = [
    ("Jake", 10, Department.DEVELOPMENT),
    ("Clare", 28, Department.SALES),
    ("Sarah", 102, Department.MARKETING),
    ("", 45, Department.HR),
]

hr_employee_with_previous_year_bonus = Employee(
    "Appa", 25, Department.HR, salary=32_000
)
hr_employee_with_previous_year_bonus.previous_bonus_years.append(2022)

employees_getting_a_raise = [
    Employee("Iroh", 70, Department.SALES, salary=25_000),
    Employee("Azula", 25, Department.SALES, salary=32_000),
    Employee("Sokka", 25, Department.FINANCE, salary=32_000),
    Employee("Aang", 25, Department.DEVELOPMENT, salary=32_000),
    Employee("Bumi", 25, Department.HR, salary=32_000),
]

employees_not_getting_a_raise = [
    Employee("Momo", 12, Department.HR),
    Employee("Zuko", 22, Department.SALES, salary=8_000),
    Employee("Roku", 98, Department.SALES, salary=32_000),
    Employee("Xiao", 25, Department.MARKETING, salary=32_000),
    Employee("Mai", 25, Department.FINANCE, salary=90_000),
    hr_employee_with_previous_year_bonus,
]
