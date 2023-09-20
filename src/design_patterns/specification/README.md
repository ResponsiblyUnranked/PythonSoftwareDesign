# The Specification Pattern

_(15 minute read)_

## Structure

| File      | Description |
| ----------- | ----------- |
| [`example.py`](example.py)      | Code examples containing anti-patterns and patterns.       |
| [`tests/best_practice_test.py`](tests/best_practice_test.py)   | Unit tests to show how the clean code works.        |
| [`tests/anti_pattern_tests.py`](tests/anti_pattern_test.py)   | Unit tests to show how the anti-patterns work.        |

## Anti-pattern

### Hiring an employee

#### Context

Throughout this example, I consider the fictional 'company' to be in the process of
hiring new employees. This 'company' has the following hiring criteria:

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

## Best Practice

### Starting at the end

Now, depending on your Python experience, the code we are going to look at could be
quite complex - I know it was for me the first time I read examples of it! So in order
to make things easier to understand, I think it's better to look at the final result
of using the specification pattern _first_.

We will look at three 'end result' examples, each of increasing complexity, and then
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
see how this has cleaned up our code a lot now. This also separates 'validating' a
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

You can see from the previous examples that all the various "criterion" classes we use
are easily interchangeable, and work like a "plug-and-play" with each other.

In order for this to be true, we need to define some common ground for these classes,
something for them to inherit from. So we start by setting up an Abstract Base Class
(ABC):

```python
class BaseSpecification(ABC):
    @abstractmethod
    def is_satisfied_by(self, employee: Employee) -> bool:
        raise NotImplementedError()
```

Next we need to expand on this ABC by allowing all class instances to be combined 
with other class instances using those logical operators, `&`, `|`, and `-`. So we 
can do this by defining [dunder methods](https://mathspp.com/blog/pydonts/dunder-methods#what-are-dunder-methods)
for these operators:

```python
class BaseSpecification(ABC):
    @abstractmethod
    def is_satisfied_by(self, employee: Employee) -> bool:
        raise NotImplementedError()

    def __and__(self, other: BaseSpecification) -> AndSpecification:
        return AndSpecification(self, other)

    def __or__(self, other: BaseSpecification) -> OrSpecification:
        return OrSpecification(self, other)

    def __neg__(self) -> NotSpecification:
        return NotSpecification(self)
```

#### Dunder methods

You will see the definition for the other classes mentioned here soon. But for now, 
let's rewrite this in a really simple manner to help explain what's going on. We'll 
focus on just the `__and__` dunder method for now:

```python
class Number():
    def __init__(self, value: int) -> None:
        self.value = value
    
    def __and__(self, other_number: Number) -> int:
        return self.value + other_number.value
```

In this small example, we have essentially turned the `&` operator into an addition 
function. So we can declare two different `Number` instances and when we use `&` 
they will be added together, because using `&` will call the `__and__` method:

```python
a = Number(3)
b = Number(4)

c = a & b  # "c" is now equal to 7 (3 + 4)
```

With the above code, you can see it resolved as the following:

```python
def __and__(self, other_number: Number) -> int:
        # `self` represents the left number in the `&` operation, 3
        # `other_number` represents the right number in the `&` operation, 4
        return self.value + other_number.value  # return 3 + 4
```

Or simply:

```python
# this
c = a & b

# is the same as this
c = a.__and__(b)
```

**The main takeaway here is that for any of these logical operators, it's called in 
that generic form:** `left_class.__operation__(right_class)`.

This same principle is applied to the `__or__` (`|`) and `__neg__` (`-`) operations too.

So if we read back at this `BaseSpecification`, we can see that each of these dunder 
methods returns a custom class for the corresponding logical operator, i.e. 
`__and__` returns an `AndSpecification` and so forth.

So let's take a look at this class:

```python
@dataclass
class AndSpecification(BaseSpecification):
    first: BaseSpecification
    second: BaseSpecification

    def is_satisfied_by(self, employee: Employee) -> bool:
        return self.first.is_satisfied_by(employee) and self.second.is_satisfied_by(
            employee
        )
```

**The very first thing I want to note is that this class _inherits_ from the** 
`BaseSpecification` **class.** This means that all the previous dunder methods we 
just looked at can be applied to this class too! As in, it's possible to do:

```python
AndSpecification(...) & AndSpecification(...)
# the result of this would be another single `AndSpecification()`
```

This is very important, as this is what allows our classes to be freely combined 
with any of the logical operators, in any order.

The only other thing to note here is how the class uses the `and` keyword to do 
exactly what we hope for:

```python
def is_satisfied_by(self, employee: Employee) -> bool:
    return self.first.is_satisfied_by(employee) and self.second.is_satisfied_by(
        employee
    )
```

An `AndSpecification(a, b)` when calling the `.is_satisfied_by(x)` will only return 
`True` if both `a.is_satisfied_by(x)` and `b.is_satisfied_by(x)` return `True`:

```python
a = ExampleSpecification()
b = ExampleSpecification()

c = AndSpecification(a, b)

# this
d = a.is_satisfied_by(x) and b.is_satisfied_by(x)

# is the same as this
d = c.is_satisfied_by(x)
```

_(The value of `x` here is irrelevant, this is to show you it would be the same 
value being passed to each one)_

### Finally

This allows us to create our actual specification classes now. So for the valid 
working age we can do the following:

```python
class IsValidWorkingAge(BaseSpecification):
    def is_satisfied_by(self, employee: Employee) -> bool:
        return 18 < employee.age < 99
```

And since it inherits the `BaseSpecification` it means this `IsValidWorkingAge` can 
use `&`, `|`, or `-` with any other class that also inherits the `BaseSpecification`.
If we also have:

```python
class HadValidName(BaseSpecification):
    def is_satisfied_by(self, employee: Employee) -> bool:
        return employee.name != ""
```

Then the following is true:

```python
age = IsValidWorkingAge()
name = HasValidName()
combined = age & name

# this
result = age.is_satisfied_by(candidate) and name.is_satisfied_by(candidate)

# is the same as this
result = combined.is_satisfied_by(candidate)
```

And behind the scenes, `combined` is an `AndSpecification` type. That last example 
should reveal how all the parts work together and allow you create complex, and 
varied specifications.

## Conclusion

The specification pattern at first may seem complicated, as you're dealing with 
multiple classes all inheriting and mixing with each other, but hopefully this 
guide is able to simplify some of the magic and provide understanding as to how you 
can create your own specifications in your code.

Take a look at the two test files to see how both code examples (anti-pattern and 
best practice) achieve the same thing, but one is much cleaner than the other.

### Additional reading

 - [Specification Pattern on Wikipedia](https://en.wikipedia.org/wiki/Specification_pattern)
 