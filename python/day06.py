import functools
import multiprocessing
from typing import Any

Position = complex
Heading = complex
Grid = dict[Position, str]


def parse_map(text: str) -> tuple[Position, Grid]:
    guard = Position()
    grid = Grid()

    for r, row in enumerate(text.splitlines()):
        for c, char in enumerate(row):
            p = Position(r, c)
            grid[p] = char
            if char == "^":
                guard = p

    return guard, grid


def rotate(heading: Heading) -> Heading:
    return Heading(heading.imag, -heading.real)


def find_visited(guard: Position, grid: Grid) -> set[Position]:
    visited: set[Position] = set()
    heading = Heading(-1, 0)

    while True:
        visited.add(guard)
        candidate = guard + heading

        if candidate not in grid:
            return visited

        if grid[candidate] == "#":
            heading = rotate(heading)
        else:
            guard = candidate


def is_loop(grid: Grid, guard: Position, extra: Position) -> bool:
    history: set[tuple[Position, Heading]] = set()
    heading = Heading(-1, 0)

    while True:
        candidate = guard + heading

        if candidate not in grid:
            return False

        if grid[candidate] == "#" or candidate == extra:
            state = (guard, heading)
            if state in history:
                return True
            history.add(state)
            heading = rotate(heading)
        else:
            guard = candidate


def run(text: str) -> tuple[Any, Any]:
    guard, grid = parse_map(text)

    visited = find_visited(guard, grid)

    with multiprocessing.Pool() as pool:
        loop_checks = pool.map(
            functools.partial(is_loop, grid, guard),
            visited - {guard},
        )

    return len(visited), loop_checks.count(True)
