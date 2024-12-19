import itertools
from collections.abc import Iterator
from typing import Any


def extract_reports(text: str) -> Iterator[list[int]]:
    for line in text.splitlines():
        yield [int(p) for p in line.split()]


def find_unsafe_index(report: list[int]) -> int | None:
    sign = 1 if report[0] > report[1] else -1

    for i, (a, b) in enumerate(itertools.pairwise(report)):
        diff = (a - b) * sign
        if diff < 1 or diff > 3:
            return i

    return None


def report_without(original: list[int], index: int) -> list[int]:
    return [level for i, level in enumerate(original) if i != index]


def run(text: str) -> tuple[Any, Any]:
    safe_count_naive = 0
    safe_count_damped = 0

    for report in extract_reports(text):
        index = find_unsafe_index(report)
        if index is None:
            safe_count_naive += 1
            safe_count_damped += 1
        elif (
            find_unsafe_index(report_without(report, index)) is None
            or find_unsafe_index(report_without(report, index - 1)) is None
            or find_unsafe_index(report_without(report, index + 1)) is None
        ):
            safe_count_damped += 1

    return safe_count_naive, safe_count_damped
