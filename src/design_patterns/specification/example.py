from src.design_patterns.specification.supplement import InvalidEmployeeError, \
    Department


class Employee:
    def __init__(
        self, name: str, age: int, department: Department, years_worked: int = 0
    ) -> None:
        self.name = name
        self.age = age
        self.department = department
        self.years_worked = years_worked

    def save(self) -> None:
        pass


# anti-pattern
def hire_new_employee(name: str, age: int, department: Department) -> Employee:
    new_employee = Employee(name, age, department)

    if (
        new_employee.age < 18
        or new_employee.age > 99
        or new_employee.department == Department.SALES
        or new_employee.name == ""
    ):
        raise InvalidEmployeeError()

    return new_employee


def give_employee_raise(employee: Employee) -> Employee:
    if employee.age < 18:
        return employee

    if employee.department == Department.SALES:
        # TODO: finish this
        pass

    return employee
