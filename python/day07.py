import operator
from collections.abc import Iterator, Callable


def extract_calibrations(data: str) -> Iterator[tuple[int, list[int]]]:
    for line in data.splitlines():
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
    results: set[int] = set(values[:1])

    for v in values[1:]:
        results = set(
            op(r, v) for op in operators for r in results if op(r, v) <= target
        )

    return target in results


def run(data: str) -> None:
    total1 = 0
    total2 = 0

    for target, values in extract_calibrations(data):
        if is_possible(target, values, operators=(operator.add, operator.mul)):
            total1 += target
        if is_possible(target, values, operators=(operator.add, operator.mul, concat)):
            total2 += target

    print(total1)
    print(total2)
