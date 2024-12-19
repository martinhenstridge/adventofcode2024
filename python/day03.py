import re
from collections.abc import Iterator
from typing import Any


def extract_multiplications(text: str, conditionals: bool) -> Iterator[tuple[int, int]]:
    enabled = True
    for m in re.finditer(r"do\(\)|don\'t\(\)|mul\((\d{1,3}),(\d{0,3})\)", text):
        match m.group(0):
            case "do()":
                enabled = True
            case "don't()":
                enabled = False
            case _:
                if enabled or not conditionals:
                    yield int(m.group(1)), int(m.group(2))


def run(text: str) -> tuple[Any, Any]:
    total_unconditional = sum(
        a * b for a, b in extract_multiplications(text, conditionals=False)
    )
    total_conditional = sum(
        a * b for a, b in extract_multiplications(text, conditionals=True)
    )

    return total_unconditional, total_conditional
