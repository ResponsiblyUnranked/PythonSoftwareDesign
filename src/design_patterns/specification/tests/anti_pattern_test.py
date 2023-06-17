import pytest

from src.design_patterns.specification.example import Employee, hire_new_employee
from src.design_patterns.specification.supplement import (
    Department,
    InvalidEmployeeError,
)
from src.design_patterns.specification.tests.fixtures import (
    invalid_new_employees,
    valid_new_employees,
)


@pytest.mark.parametrize("name,age,department", valid_new_employees)
def test_can_hire_new_employee(name: str, age: int, department: Department) -> None:
    # when
    employee = hire_new_employee(name, age, department)

    # then
    assert isinstance(employee, Employee)


@pytest.mark.parametrize("name,age,department", invalid_new_employees)
def test_error_raised_for_invalid_employee(
    name: str, age: int, department: Department
) -> None:
    # then
    with pytest.raises(InvalidEmployeeError):
        # when
        hire_new_employee(name, age, department)
