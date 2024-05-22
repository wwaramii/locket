from collections.abc import Sequence
from typing import TypeVar

T = TypeVar("T")


def create_keyboard_layout(buttons: Sequence[T], schema: Sequence[int]) -> list[list[T]]:
    """
    a simple keyboard layout creator based on the provided scheme.
    """
    if sum(schema) != len(buttons):
        raise ValueError("Invalid schema.")
    layout: list[list[T]] = []
    btn_number = 0
    for a in schema:
        layout.append([])
        for _ in range(a):
            layout[-1].append(buttons[btn_number])
            btn_number += 1
    return layout