from collections.abc import Iterator
from typing import Any


class Page:
    def __init__(self, n: str, rules: set[tuple[int, int]]) -> None:
        self.n = int(n)
        self.rules = rules

    def __eq__(self, other: Any) -> bool:
        assert isinstance(other, Page)
        return self.n == other.n

    def __lt__(self, other: "Page") -> bool:
        return (self.n, other.n) in self.rules


def extract_rules(data: str) -> set[tuple[int, int]]:
    rules = set()
    for line in data.splitlines():
        n1, n2 = line.split("|", maxsplit=1)
        rule = int(n1), int(n2)
        rules.add(rule)
    return rules


def extract_pages(data: str, rules: set[tuple[int, int]]) -> Iterator[list[Page]]:
    for line in data.splitlines():
        yield [Page(n, rules) for n in line.split(",")]


def run(data: str) -> None:
    rule_data, page_data = data.split("\n\n", maxsplit=1)
    rules = extract_rules(rule_data)

    sum1 = 0
    sum2 = 0
    for pages in extract_pages(page_data, rules):
        middle = len(pages) // 2
        ordered = sorted(pages)
        if ordered == pages:
            sum1 += ordered[middle].n
        else:
            sum2 += ordered[middle].n

    print(sum1)
    print(sum2)
