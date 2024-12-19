import functools
from collections.abc import Callable
from typing import Any

CountFn = Callable[[list[str], str], int]


def memoize(fn: CountFn) -> CountFn:
    cache: dict[str, int] = {}

    @functools.wraps(fn)
    def wrapper(towels: list[str], target: str) -> int:
        if target not in cache:
            cache[target] = fn(towels, target)
        return cache[target]

    return wrapper


@memoize
def count_combinations(towels: list[str], target: str) -> int:
    if not target:
        return 1

    ways = 0
    for towel in towels:
        if target.startswith(towel):
            ways += count_combinations(towels, target[len(towel) :])

    return ways


def run(text: str) -> tuple[Any, Any]:
    towel_text, design_text = text.split("\n\n", maxsplit=1)

    towels = towel_text.split(", ")
    designs = design_text.splitlines()

    possible = 0
    different = 0
    for design in designs:
        count = count_combinations(towels, design)
        different += count
        if count != 0:
            possible += 1

    return possible, different
