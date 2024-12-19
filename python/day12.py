import itertools
from collections import defaultdict
from collections.abc import Iterator, Mapping
from typing import Any


def extract_plots(text: str) -> Mapping[complex, str]:
    plots: dict[complex, str] = {}
    for r, row in enumerate(text.splitlines()):
        for c, char in enumerate(row):
            plots[complex(r, c)] = char
    return plots


def get_neighbours(plot: complex) -> Iterator[complex]:
    yield from (
        plot + complex(0, -1),
        plot + complex(0, +1),
        plot + complex(-1, 0),
        plot + complex(+1, 0),
    )


def find_fence(region: set[complex]) -> Mapping[tuple[complex, complex], list[int]]:
    fence: defaultdict[tuple[complex, complex], list[int]] = defaultdict(list)

    for p in region:
        for n in get_neighbours(p):
            if n not in region:
                if p.real == n.real:
                    shared = (complex(0, p.imag), complex(0, n.imag))
                    unique = int(p.real)
                else:
                    shared = (complex(p.real, 0), complex(n.real, 0))
                    unique = int(p.imag)
                fence[shared].append(unique)

    return fence


def find_regions(plots: Mapping[complex, str]) -> Iterator[set[complex]]:
    ungrouped = set(plots)

    while ungrouped:
        plot = ungrouped.pop()
        crop = plots[plot]

        region: set[complex] = {plot}
        border: set[complex] = {plot}

        while border:
            p = border.pop()
            for n in get_neighbours(p):
                if n not in plots:
                    continue
                if n not in ungrouped:
                    continue
                if plots[n] == crop:
                    ungrouped.discard(n)
                    region.add(n)
                    border.add(n)

        yield region


def run(text: str) -> tuple[Any, Any]:
    plots = extract_plots(text)

    total1 = 0
    total2 = 0
    for region in find_regions(plots):
        fence = find_fence(region)
        perimeter = 0
        sides = 0

        for panels in fence.values():
            perimeter += len(panels)
            sides += 1
            for a, b in itertools.pairwise(sorted(panels)):
                if b - a > 1:
                    sides += 1

        area = len(region)
        total1 += area * perimeter
        total2 += area * sides

    return total1, total2
