import itertools
from collections.abc import Iterator


def parse_map(data: str) -> tuple[complex, dict[complex, str]]:
    guard: complex = complex(0)
    grid: dict[complex, str] = {}

    for r, row in enumerate(data.splitlines()):
        for c, char in enumerate(row):
            p = complex(real=r, imag=c)
            grid[p] = char
            if char == "^":
                guard = p

    return guard, grid


def heading_cycler() -> Iterator[complex]:
    return itertools.cycle(
        (
            complex(real=-1, imag=0),
            complex(real=0, imag=1),
            complex(real=1, imag=0),
            complex(real=0, imag=-1),
        )
    )


def count_visited(guard: complex, grid: dict[complex, str]) -> int:
    heading_iter = heading_cycler()
    heading = next(heading_iter)

    visited: set[complex] = set()

    while True:
        visited.add(guard)
        candidate = guard + heading

        if candidate not in grid:
            break

        if grid[candidate] == "#":
            heading = next(heading_iter)
        else:
            guard = candidate

    return len(visited)


def is_loop(guard: complex, grid: dict[complex, str]) -> bool:
    heading_iter = heading_cycler()
    heading = next(heading_iter)

    history: set[tuple[complex, complex]] = set()

    while True:
        if (guard, heading) in history:
            return True

        history.add((guard, heading))
        candidate = guard + heading

        if candidate not in grid:
            return False

        if grid[candidate] == "#":
            heading = next(heading_iter)
        else:
            guard = candidate

    return False


def run(data: str) -> None:
    guard, grid = parse_map(data)

    visited = count_visited(guard, grid)

    loops = 0
    for p in grid:
        if grid[p] != ".":
            continue

        grid[p] = "#"
        if is_loop(guard, grid):
            loops += 1
        grid[p] = "."

    print(visited)
    print(loops)
