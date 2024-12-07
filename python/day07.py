import operator
from collections.abc import Iterator, Callable


def extract_calibrations(data: str) -> Iterator[tuple[int, list[int]]]:
    for line in data.splitlines():
        left, right = line.split(": ")
        yield int(left), [int(v) for v in right.split()]


def concat(a: int, b: int) -> int:
    return int(str(a) + str(b))


def analyse(
    target: int, values: list[int], ops: tuple[Callable[[int, int], int], ...]
) -> bool:
    results: set[int] = set(values[:1])

    for value in values[1:]:
        updated = set()
        for op in ops:
            updated |= set(op(r, value) for r in results)
        results = updated

    return target in results


def run(data: str) -> None:
    total1 = 0
    total2 = 0

    for result, values in extract_calibrations(data):
        if analyse(result, values, ops=(operator.add, operator.mul)):
            total1 += result
        if analyse(result, values, ops=(operator.add, operator.mul, concat)):
            total2 += result

    print(total1)
    print(total2)
