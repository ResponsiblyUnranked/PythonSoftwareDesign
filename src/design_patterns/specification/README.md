# The Specification Pattern

## Structure

| File      | Description |
| ----------- | ----------- |
| [`example.py`](example.py)      | Code examples containing anti-patterns and patterns.       |
| [`tests/best_practice_test.py`](tests/best_practice_test.py)   | Unit tests to show how the clean code works.        |
| [`tests/anti_pattern_tests.py`](tests/anti_pattern_test.py)   | Unit tests to show how the anti-patterns work.        |

## Anti-pattern

### Hiring an employee

#### Context

Throughout this example, I consider the fictional "company" to be in the process of
hiring new employees. This "company" has the following hiring criteria:

 - Candidate is over 18 years old and
 - Candidate is under 99 years old
 - Candidate is not applying for a role in the sales department
 - Candidate has a non-empty name

#### Code

Let's take a look at the initial hiring function:

```python
def hire_new_employee_anti_pattern(
    name: str, age: int, department: Department
) -> Employee:
    new_employee = Employee(name, age, department)

    if (
        new_employee.age < 18
        or new_employee.age > 99
        or new_employee.department == Department.SALES
        or new_employee.name == ""
    ):
        raise InvalidEmployeeError()

    return new_employee
```

This code is simple, easy to read and understand, and does the job with minimal lines
of code. So what's the issue?

Well, what if we now want each company department to be in charge of their own criteria?
We would have to create more functions for every single department.

## Best practice

## Conclusion

### Additional reading

 - [Specification Pattern on Wikipedia](https://en.wikipedia.org/wiki/Specification_pattern)
 