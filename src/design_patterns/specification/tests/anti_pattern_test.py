import pytest

from src.design_patterns.specification.example import Employee, hire_new_employee, \
    is_employee_eligible_for_a_raise
from src.design_patterns.specification.supplement import (
    Department,
    InvalidEmployeeError,
)
from src.design_patterns.specification.tests.fixtures import (
    invalid_new_employees,
    valid_new_employees, employees_getting_a_raise, employees_not_getting_a_raise,
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


@pytest.mark.parametrize("employee", employees_getting_a_raise)
def test_employee_is_eligible_for_a_raise(employee: Employee) -> None:
    # when
    is_getting_raise = is_employee_eligible_for_a_raise(employee)

    # then
    assert is_getting_raise


@pytest.mark.parametrize("employee", employees_not_getting_a_raise)
def test_employee_is_not_eligible_for_a_raise(employee: Employee) -> None:
    # when
    is_getting_raise = is_employee_eligible_for_a_raise(employee)

    # then
    assert not is_getting_raise
