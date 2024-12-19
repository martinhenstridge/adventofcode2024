import operator
from collections.abc import Callable, Iterator
from typing import Any


def extract_calibrations(text: str) -> Iterator[tuple[int, list[int]]]:
    for line in text.splitlines():
        left, right = line.split(": ")
        yield int(left), [int(v) for v in right.split()]


def concat(a: int, b: int) -> int:
    digits = b
    while digits:
        digits //= 10
        a *= 10
    return a + b


def is_possible(
    target: int, values: list[int], operators: tuple[Callable[[int, int], int], ...]
) -> bool:
    results: list[int] = values[:1]

    for v in values[1:]:
        updated: list[int] = []
        for op in operators:
            for r in results:
                new = op(r, v)
                if new <= target:
                    updated.append(new)
        results = updated

    return target in results


def run(text: str) -> tuple[Any, Any]:
    total1 = 0
    total2 = 0

    for target, values in extract_calibrations(text):
        if is_possible(target, values, operators=(operator.add, operator.mul)):
            total1 += target
        if is_possible(target, values, operators=(operator.add, operator.mul, concat)):
            total2 += target

    return total1, total2
