from collections import defaultdict
from collections.abc import Iterator, Mapping
from typing import Any


def parse_grid(text: str) -> Mapping[complex, int]:
    return {
        complex(r, c): int(char)
        for r, row in enumerate(text.splitlines())
        for c, char in enumerate(row)
    }


def neighbours(p: complex) -> Iterator[complex]:
    yield p + complex(-1, 0)
    yield p + complex(0, -1)
    yield p + complex(0, +1)
    yield p + complex(+1, 0)


def find_reachable(grid: Mapping[complex, int], p0: complex) -> Mapping[complex, int]:
    trails: defaultdict[complex, int] = defaultdict(int)
    trails[p0] += 1

    for h in range(1, 10):
        if not trails:
            break

        trails_next: defaultdict[complex, int] = defaultdict(int)
        for t, count in trails.items():
            for p in neighbours(t):
                if p not in grid:
                    continue
                if grid[p] == h:
                    trails_next[p] += count
        trails = trails_next

    return trails


def run(text: str) -> tuple[Any, Any]:
    grid = parse_grid(text)

    total1 = 0
    total2 = 0

    for p, h in grid.items():
        if h == 0:
            reachable = find_reachable(grid, p)
            total1 += len(reachable)
            total2 += sum(reachable.values())

    return total1, total2
