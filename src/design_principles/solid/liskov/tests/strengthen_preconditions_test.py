import pytest

from src.design_principles.solid.liskov.detailed.strengthen_preconditions import Parrot, FussyParrot


def test_normal_parrot_can_repeat_number() -> None:
    # given
    my_pet = Parrot("Peter")
    number = 5

    # when
    speech = my_pet.speak_number(number)

    # then
    assert str(number) in speech


def test_normal_parrot_can_repeat_negative_number() -> None:
    # given
    my_pet = Parrot("Peter")
    number = -4

    # when
    speech = my_pet.speak_number(number)

    # then
    assert str(number) in speech


def test_fussy_parrot_can_repeat_number() -> None:
    # given
    my_pet = FussyParrot("Percy")
    number = 5

    # when
    speech = my_pet.speak_number(number)

    # then
    assert str(number) in speech


@pytest.mark.xfail(reason="This test demonstrates an anti-pattern.")
def test_fussy_parrot_fails_to_repeat_negative_number() -> None:
    # given
    my_pet = FussyParrot("Percy")
    number = -4

    # when
    speech = my_pet.speak_number(number)

    # then
    assert str(number) in speech
