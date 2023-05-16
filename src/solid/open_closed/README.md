# Open / Closed Principle

## Structure

| File      | Description |
| ----------- | ----------- |
| [`./example.py`](example.py)      | Code examples containing anti-patterns and patterns.       |
| [`./supplement.py`](supplement.py)     | Additional code to assist in the examples. You don't need to read this to learn the pattern.        |
| [`tests/open_closed_test.py`](../../../tests/solid_single_responsibility_test.py)   | Unit tests to show code in action.        |

## Anti-pattern

Take a look at `JuniorTeacher` in `example.py`. We've got a teacher that has a `name`
and can teach a class with `.teach_class()`. Now if you look at the tests, this may
seem like a good way of doing things, as a teacher can teach whatever you want with:

```python
teacher = JuniorTeacher(name="Maurice Moss")
teacher.teach_class("maths")
```

And we can just replace `"maths"` with any other subject! Especially with
that final return statement in the definition of `.teach_class()` we can freestyle with
any subject:

```python
return f"{self.name} is freestyling and teaching {subject}!"
```

Unfortunately, no matter how good this flexibility may seem, this code follows the very
opposite of the Open/Closed principle.

The principle suggests that classes/interfaces should be **open for extension, but 
closed to modification.**

`JuniorTeacher` directly breaks this principle, because if we want to add more lesson
plans for different subjects, we have to **modify** the class rather than **expanding**
it. And modification is often bad because it could break your code, whereas extension
aims to allow you to add functionality without breaking existing code.

### How can modifying our example break it?

At present, our `JuniorTeacher` can only teach maths and science, and will freestyle a
lesson plan for any other subjects. But let's say we want to allow our teacher to
teach biology:

```python
def teach_class(self, subject: str) -> str:
    if subject == "maths":
        return f"{self.name} is teaching algebra!"

    if subject == "science":
        return f"{self.name} is teaching particle physics!"

    if subject == "biology":
        return f"{self.name} is teaching the human anatomy!"

    return f"{self.name} is freestyling and teaching {subject}!"
```

This doesn't make as much sense now, since we could consider biology a "science". So we
should probably change `"science"` to something more specific, like `"physics"`.

And this is where we meet the problem. If we want to add a new subject, or change some
subjects, we have to risk breaking how the other subjects work!

Changing `"science"` to `"physics"` would break our test, as it was expecting a
different value (this test is simulating us breaking some other part of our program):

```shell
tests/open_closed_test.py:23 (test_junior_teacher_can_teach_science)
Maurice Moss is freestyling and teaching science! != Maurice Moss is teaching particle physics!

Expected :Maurice Moss is teaching particle physics!
Actual   :Maurice Moss is freestyling and teaching science!
<Click to see difference>

def test_junior_teacher_can_teach_science() -> None:
        # given
        teacher_name = "Maurice Moss"
        teacher = JuniorTeacher(name=teacher_name)
    
        # when
        lesson = teacher.teach_class("science")
    
        # then
>       assert lesson == f"{teacher_name} is teaching particle physics!"
E       AssertionError: assert 'Maurice Moss is freestyling and teaching science!' == 'Maurice Moss is teaching particle physics!'

tests/open_closed_test.py:33: AssertionError
```

As [this article neatly puts it](http://joelabrahamsson.com/a-simple-example-of-the-openclosed-principle/#:~:text=we%20should%20strive%20to%20write%20code%20that%20doesn%E2%80%99t%20have%20to%20be%20changed%20every%20time%20the%20requirements%20change)
(emphasis mine):

> ...we should strive to write code that doesn't ***have*** to be changed every time the 
> requirements change.

We can't guarantee that our code will _never_ have to be modified, but the aim is to
write code that can easily be _expanded upon_ in favour of being modified.

In our example, the requirements changed such that we needed to add a new subject,
biology, to the subjects that a teacher could teach. But in order to do this, we had
to **change** the existing `.teach_class()`. Let's take a look at the best practice
to see how we can improve on this example.

## Best Practice

Looking at our `SeniorTeacher` class, it should become clear how this is
an improvement from `JuniorTeacher`. Immediately, we can see that **teaching a class no
longer depends on a particular subject**.

If only look at the inputs and outputs of the method, known as the **method signature**
then we can see that there is no dependency on a subject:

```python
def teach_class(self) -> str:
```

We are free to teach a class as we please, without needing to worry about the subject.
And what this ultimately means, is that we no longer need to change `.teach_class()` if
we want to add more subjects.

Instead, our `.teach_class()` method now depends on the `Subject` interface:

```python
class Subject(Protocol):
    def get_lesson_plan(self) -> str:
        ...
```

We inherit Python's `Protocol` class to indicate that this class is an _interface_.
This means several things:
 - We don't define any logic in the class, only **method signatures** (and property
types)
 - The class isn't instantiated itself, instead it's only used as a type hint
 - Any other class that **implements** these methods will be treated as a `Subject`
class

This is known as [duck typing](https://en.wikipedia.org/wiki/Duck_typing), because:

> If it walks like a duck, and it quacks like a duck, then it must be a duck.

So in our example, ***any*** class that has a `.get_lesson_plan()` method that takes
exactly zero arguments, and returns a string, will be considered a `Subject`.

So although `Maths` doesn't inherit from `Subject` or mention it in any way, it can be
treated as a `Subject` class, because it implements that `.get_lesson_plan()` method:

```python
class Maths:
    def get_lesson_plan() -> str:
        return "algebra"
```

And we are now free to create new lesson plans as we see fit, without having to modify
`SeniorTeacher` in any way. A music class could look like:

```python
class Music:
    def get_lesson_plan() -> str:
        return "chord structures"
```

## Conclusion

Hopefully this shows that if we think about the designs of our class carefully, we can
avoid having to _modify_ existing code when _extending_ the functionality - extending
functionality should extend the code (in most cases).

### Additional reading

 - [Another example of the Open/Closed Principle in Python on GitHub](https://github.com/heykarimoff/solid.python/blob/master/2.ocp.py)
 - [ArjanCodes on SOLID Principles](https://www.youtube.com/watch?v=pTB30aXS77U)
 