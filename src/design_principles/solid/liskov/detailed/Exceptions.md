# Detailed Liskov Substitution

_(2 minute read)_

## Structure

| File      | Description |
| ----------- | ----------- |
| [`exceptions.py`](exceptions.py)      | Code example containing a pattern and anti-pattern.       |
| [`../tests/exceptions_test.py`](../tests/exceptions_test.py)   | Unit tests to show code in action.        |

## Exceptions

When inheriting from a class, all exceptions raised by a method should match, or be a
subtype of the original exception raised in the parent class.

This is because if you have code that is in a try/except block, the exception it is
expecting to catch could be a generic one and so if you raise that exception, or a
subtype of that exception then everything will work fine. But if you raise a different
type of exception then the error will slip through your try/except and crash your
program.

The following short example should make this easy to understand.

### The example

Our example is about a file system class that can read the files on a computer.
As you can see, we have three types:

 - A generic `SystemFileReader`
 - A reader specific to Microsoft Windows: `WindowsFileReader`
 - And a reader specific to Apple Mac OSX: `MacOSFileReader`

The Windows and MacOS classes are a subclass of the generic system, so any errors 
that these subclasses raise should match or be a subclass of the errors that are 
raised in the corresponding methods of the parent class.

Let's look at our tests to see this in action:

```python
def test_normal_exceptions_are_caught() -> None:
    # given
    reader = SystemFileReader()

    try:
        # when
        reader.open_file(Path("test.txt"))
    except FileError:
        # then
        assert True
```

This first test demonstrates how some typical code might work. We are using the 
generic class, and we know that a `FileError` may occur, so we have some code to 
check for this and compensate for it. The test passes fine.

```python
def test_subclass_follows_liskov() -> None:
    # given
    reader = WindowsFileReader()

    try:
        # when
        reader.open_file(Path("test.txt"))
    except FileError:
        # then
        assert True
```

Our next test uses the Windows class, and if you look at the original code, this 
actually raises a `MissingFileError`. You may have also noticed that the code in 
this test is the exact same as the first test. This is because if Liskov is followed 
correctly, you _should_ be able to swap these classes and subclasses without any 
issues!

And so because `MissingFileError` is a subclass of `FileError`, this test also 
passes fine.

Our problem comes when we look at the MacOS test:

```python
def test_subclass_breaks_liskov() -> None:
    # given
    reader = MacOSFileReader()

    try:
        # when
        reader.open_file(Path("test.txt"))
    except FileError:
        # then
        assert True
```

The code again looks the same, but the test fails because the MacOS code raises a 
`ValueError` which is not a subclass of `FileError`. This means that the exception 
slips through our try/except block and crashes our program!

## Conclusion

This quick guide should give you an idea for how exceptions can slip through our 
client code if they do not also follow the LSP.