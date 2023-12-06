from typing import Dict

from src.design_patterns.command.photoshop_example import (
    Command,
    KeyboardHandler,
    PhotoshopToolSelector,
    SelectBrush,
    SelectEraser,
)


def test_can_use_commands() -> None:
    # given
    tool_selector = PhotoshopToolSelector()

    key_bindings: Dict[str, Command] = {
        "b": SelectBrush(tool_selector),
        "e": SelectEraser(tool_selector),
    }

    key_handler = KeyboardHandler(key_bindings)

    # then
    key_handler.handle_input("b")
    key_handler.handle_input("e")


def test_unbound_keys_do_not_raise_error() -> None:
    # given
    tool_selector = PhotoshopToolSelector()

    key_bindings: Dict[str, Command] = {
        "b": SelectBrush(tool_selector),
        "e": SelectEraser(tool_selector),
    }

    key_handler = KeyboardHandler(key_bindings)

    # then
    key_handler.handle_input("x")
