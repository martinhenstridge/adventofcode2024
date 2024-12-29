import functools
import multiprocessing
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
    target: int,
    values: list[int],
    *,
    operators: tuple[Callable[[int, int], int], ...],
) -> int:
    results: list[int] = values[:1]

    for v in values[1:]:
        updated: list[int] = []
        for op in operators:
            for r in results:
                new = op(r, v)
                if new <= target:
                    updated.append(new)
        results = updated

    return target if target in results else 0


def run(text: str) -> tuple[Any, Any]:
    calibrations = list(extract_calibrations(text))

    with multiprocessing.Pool() as pool:
        possibles1 = pool.starmap(
            functools.partial(
                is_possible,
                operators=(operator.add, operator.mul),
            ),
            calibrations,
        )
        possibles2 = pool.starmap(
            functools.partial(
                is_possible,
                operators=(operator.add, operator.mul, concat),
            ),
            calibrations,
        )

    return sum(possibles1), sum(possibles2)
