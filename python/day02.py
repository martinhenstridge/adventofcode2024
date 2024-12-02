import itertools
from collections.abc import Iterator


def extract_reports(data: str) -> Iterator[list[int]]:
    for line in data.splitlines():
        yield [int(p) for p in line.split()]


def find_unsafe_pair(report: list[int]) -> tuple[int, int] | None:
    sign = 1 if report[0] > report[1] else -1

    for i, (a, b) in enumerate(itertools.pairwise(report)):
        diff = (a - b) * sign
        if diff < 1:
            return i, i + 1
        if diff > 3:
            return i, i + 1

    return None


def report_without(report: list[int], index: int) -> list[int]:
    return [level for i, level in enumerate(report) if i != index]


def run(data: str) -> None:
    safe_count_naive = 0
    safe_count_damped = 0

    for report in extract_reports(data):
        unsafe = find_unsafe_pair(report)
        if not unsafe:
            safe_count_naive += 1
            safe_count_damped += 1
        elif (
            find_unsafe_pair(report_without(report, unsafe[0])) is None
            or find_unsafe_pair(report_without(report, unsafe[1])) is None
        ):
            safe_count_damped += 1

    print(safe_count_naive)
    print(safe_count_damped)
