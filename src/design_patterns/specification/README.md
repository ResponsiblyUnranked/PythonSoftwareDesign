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
We would have to create more functions for every single department, and we'd end up
repeating ourselves a lot if all these different departments wanted to use the same
basic criteria for hiring employees.

### Determining raise eligibility

The following code shows a better example of why allowing each department to determine
their own criteria can become difficult to manage:

```python
def is_employee_eligible_for_a_raise_anti_pattern(employee: Employee) -> bool:
    if employee.age < 18 or employee.age > 99:
        return False

    if employee.department == Department.SALES:
        if employee.salary < 10_000:
            return False

        if employee.salary >= 10_000:
            if employee.age >= 75:
                return False
            else:
                return True

    elif employee.department == Department.FINANCE:
        if employee.salary > 85_000:
            return False
        return True

    elif employee.department == Department.DEVELOPMENT:
        return True

    elif employee.department == Department.HR:
        for year in employee.previous_bonus_years:
            if year == 2022:
                return False
        return True

    return False
```

This is code is a bit more difficult to read, and it's harder to find what you're
looking for if you're trying to work on a specific part of code. Now what would this
function look like if we had a global company with hundreds of departments across
several continents? You can see it  quickly becomes a really long function trying to
tackle too many things at once.

What we really need, is some dynamic way of defining these criteria in a way that
allows us to not only _reuse_ them, but _mix and match_ them to create any sort of
custom criteria we like. Wouldn't it be nice if we could cluster different criteria
into a single variable, which can be easily replaced?

This is where the specification pattern comes in!

## Best practice

### Starting at the end

Now, depending on your Python experience, the code we are going to look at could be
quite complex - I know it was for me the first time I read examples of it! So in order
to make things easier to understand, I think it's better to look at the final result
of using the specification pattern _first_.

We will look at three "end result" examples, each of increasing complexity, and then
we will tackle how you write these classes so that they can be used in this way.

#### Example #1

```python
def hire_new_employee_simple(name: str, age: int, department: Department) -> Employee:
    hiring_specification = MatchesHiringCriteria()
    new_employee = Employee(name, age, department)

    if hiring_specification.is_satisfied_by(new_employee):
        return new_employee

    raise InvalidEmployeeError()
```

Without going into the implementation details yet, the above code does exactly the same
thing as the very first code example in this guide.
`MatchesHiringCriteria().is_satisfied_by(...)` performs the exact same checks.

Okay, so you're probably thinking that I've just moved that original function to be a
method on the `MatchesHiringCriteria()` class right? Well, I have, but you can already
see how this has cleaned up our code a lot now. This also separates "validating" a
potential candidate, from actually hiring them.

But if we want to adjust these criteria, we still have to change this entire method
which is checking lots of different criteria. 

#### Example #2

This next example shows how we can separate each criterion into its own class.
Again, this function performs exactly the same as the previous one:

```python
def hire_new_employee_granular(name: str, age: int, department: Department) -> Employee:
    hiring_specification = (
        IsValidWorkingAge()
        & HadValidName()
        & -BelongsToDepartment(Department.SALES)
    )

    new_employee = Employee(name, age, department)

    if hiring_specification.is_satisfied_by(new_employee):
        return new_employee

    raise InvalidEmployeeError()
```

And this is where the real beauty of the specification pattern comes in. You can see
that `hiring_specification` is now a combination of several classes.

We are using the
bitwise "AND" operator, which is the `&` (ampersand) in the code. If you've not seen 
or used this in Python before don't worry - in this example you can think of it like 
the `and` keyword (but you cannot swap them for each other as they are not the 
same thing, please read more about this
[here](https://www.geeksforgeeks.org/difference-between-and-and-in-python/) and
[here](https://en.wikipedia.org/wiki/Bitwise_operation)).

Now you can see the above example has a separate class for each criterion, but they
still represent the same principles we outlined at the start:

 - Candidate is over 18 years old and
 - Candidate is under 99 years old

are now represented by `IsValidWorkingAge()`,

 - Candidate has a non-empty name

is represented by `HasValidName()`, and

 - Candidate is not applying for a role in the sales department

is represented by `-BelongsToDepartment()`. Notice that we named this last criterion
as _belonging_ to a particular department? This is because it is good to stay consistent
with the positive, accepting sentiment of our criteria.

What I mean by this, is each criterion checks that some `A` value is `B`, rather than
checking that `A` **is not** `B`. Which of the following is easier to read?

| Positive Sentiment | Negative Sentiment |
| ------------------ | ------------------ |
| <ul><li>`IsValidWorkingAge`</li><li>`HasValidName`</li><li>`BelongsToDepartment`</li></ul> | <ul><li>`IsNotInvalidAge`</li><li>`NoInvalidCharactersInName`</li><li>`DoesNotBelongToDepartment`</li></ul> |

As you can see, it's generally easier to understand, and easier to be more concise with
your wording (it also follows good grammar by avoiding double negatives).
This is probably not always the case, but we also highly value consistency
in programming, and since the first two criteria follow this positive sentiment, let's
continue this for `BelongsToDepartment`.

Now, because we are using this positive sentiment, it doesn't actually fit our criteria
of:

 - Candidate is **not** applying for a role in the sales department

But that is why we have the little `-` (minus) before the class. This acts as a "NOT"
operator. Again, for simplicity you can think of this like the `not` keyword in Python,
but the same points should be noted for the `-` operator as for the `&` operator.

Hopefully the benefits of separating the criteria into their own classes is clear. I can
think of three main things we gain by doing this:

 - If we need to redefine what a "valid working age" is, we can adjust this in the 
individual class, without affecting any other code, or needing to change any other code
 - If we no longer want to exclude applicants for the sales department, it's as simple
as removing that last class `-BelongsToDepartment(Department.SALES)`
 - We are free to re-use these various criteria in other parts of code, while still only
having a single definition of "valid working age" for example

#### Example #3

This last example shows how easy it is to create separate specifications for each
department and combine them together:

```python
def is_employee_eligible_for_a_raise(employee: Employee) -> bool:
    raise_specification = (
        SalesRaiseEligibility()
        | FinanceRaiseEligibility()
        | DevelopmentRaiseEligibility()
        | HrRaiseEligibility()
    ) & IsValidWorkingAge()

    return raise_specification.is_satisfied_by(employee)
```

Like in previous examples, we are using another bitwise operator. The `|` (pipe) is
the bitwise "OR" operator, and also like in the previous examples, can be thought of
as the `or` keyword in Python for simplicity.

This `raise_specification` now shows you only need to be eligible for one of the
department's raise criteria, as well as always being a valid working age.

Like with the second example, this should make it clear how easy it is to adjust one
department's definition of being "eligible" for a raise while not having to touch the
code relating to other departments. It also allows us to remove a particular
department's criteria if they are not handing out raises in a given year.

### So how do we create these classes?

## Conclusion

### Additional reading

 - [Specification Pattern on Wikipedia](https://en.wikipedia.org/wiki/Specification_pattern)
 