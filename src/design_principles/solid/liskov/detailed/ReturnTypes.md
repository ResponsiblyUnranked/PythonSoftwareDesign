# Detailed Liskov Substitution

_(2 minute read)_

## Structure

| File      | Description |
| ----------- | ----------- |
| [`return_types.py`](return_types.py)      | Code example containing an anti-pattern.       |
| [`../tests/return_types_test.py`](../tests/return_types_test.py)   | Unit tests to show code in action.        |

## Return Types

When inheriting from a class, all method return types should match, or be _more_
specific than the superclass (parent) method return type.

This is opposite to the [parameter types](ParameterTypes.md) section. In that section
we learnt that the subclass method must have arguments that match, or are more abstract
than the superclass. But here, we learn that the subclass method should have a return
type that matches, or is more specific than the superclass.

### The problem

Before we start, let's remind ourselves of the core idea of the Liskov substitution 
principle (LSP), which is that:

> ...objects of a superclass should be replaceable with objects of its subclasses 
> without breaking the application.

With that in mind let's take a look at a unit test:

```python
def test_can_save_game_from_rental_store() -> None:
    # given
    rental_store = GameRentalStore()

    # when
    my_game = rental_store.rent_game("GoldenEye")

    # then
    my_game.save()
```

This test works fine. So why don't we try another one with an `IndieGameRentalStore`
instead? Since this is a subclass of `GameRentalStore`:

```python
def test_can_save_game_from_indie_rental_store() -> None:
        # given
        rental_store = IndieGameRentalStore()
    
        # when
        my_game = rental_store.rent_game("GoldenEye")
    
        # then
>       my_game.save()  # type: ignore[attr-defined]
E       AttributeError: 'Game' object has no attribute 'save'
```

Again, we've broken the LSP here. Take a look inside the example code to see how.

We can see that the `GameRentalStore.rent_game()` method will return a `VideoGame`
instance, a subclass of `Game`. The `IndieGameRentalStore.rent_game()` method however,
returns a `Game` type. This is more abstract than the parent `GameRentalStore.rent_game()`
method.

It's the being "more abstract" here that is breaking the LSP. Because `Game` is more 
abstract than `VideoGame`, it isn't guaranteed to have all the methods/properties that
`VideoGame` has.

So in our case, the `.save()` method is only implemented in `VideoGame`. This 
hopefully highlights why the return types cannot be more abstract than the parent 
class.

### The solution

The return type should match, or be more specific. So our
`IndieGameRentalStore.rent_game()` should return either a `VideoGame` instance or 
something more specific. This ensures that the `.save()` method still exists.

Something more specific could look like:

```python
class XboxGame(VideoGame):
    def connect_online(self) -> Connection:
        ...
```

So `IndieGameRentalStore.rent_game()` could return an `XboxGame` instance because it 
inherits from `VideoGame`, so it will still have the `.save()` method.
