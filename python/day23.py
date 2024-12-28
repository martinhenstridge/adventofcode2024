from collections import defaultdict
from typing import Any


def parse_computers(text: str) -> dict[str, set[str]]:
    computers = defaultdict(set)
    for line in text.splitlines():
        a, b = line.split("-", maxsplit=1)
        computers[a].add(b)
        computers[b].add(a)
    return computers


def find_trios(computers: dict[str, set[str]]) -> set[frozenset[str]]:
    trios = set()

    for a in computers:
        if not a.startswith("t"):
            continue
        for b in computers[a]:
            for c in computers[b]:
                if a in computers[c]:
                    trio = frozenset([a, b, c])
                    trios.add(trio)

    return trios


def find_groups(computers: dict[str, set[str]]) -> list[set[str]]:
    groups = [{c} for c in computers]

    for candidate, connections in computers.items():
        for group in groups:
            if connections >= group:
                group.add(candidate)

    return groups


def run(text: str) -> tuple[Any, Any]:
    computers = parse_computers(text)

    trios = find_trios(computers)
    part1 = len(trios)

    groups = find_groups(computers)
    lan = max(groups, key=len)
    part2 = ",".join(sorted(lan))

    return part1, part2
