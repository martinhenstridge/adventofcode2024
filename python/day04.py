from collections.abc import Iterator
from typing import Any


class Grid:
    _data: list[str]
    _size: int

    def __init__(self, text: str) -> None:
        self._data = text.splitlines()
        self._size = len(self._data)

    def __iter__(self) -> Iterator[tuple[int, int]]:
        for r in range(self._size):
            for c in range(self._size):
                yield r, c

    def check(self, target: str, r: int, c: int) -> bool:
        if r < 0:
            return False
        if c < 0:
            return False
        if r >= self._size:
            return False
        if c >= self._size:
            return False
        return self._data[r][c] == target

    def mas(self, r: int, c: int, dr: int, dc: int) -> bool:
        for target in "MAS":
            if not self.check(target, r, c):
                return False
            r += dr
            c += dc
        return True


def xmas_count(grid: Grid, r: int, c: int) -> int:
    if not grid.check("X", r, c):
        return 0

    count = 0
    for dr, dc in (
        (-1, 0),
        (0, +1),
        (+1, 0),
        (0, -1),
        (-1, +1),
        (+1, +1),
        (+1, -1),
        (-1, -1),
    ):
        if grid.mas(r + dr, c + dc, dr, dc):
            count += 1
    return count


def x_mas_count(grid: Grid, r: int, c: int) -> int:
    # All X-MAS instances have an A at the centre
    if not grid.check("A", r, c):
        return 0

    # Check for \-oriented MAS
    if not (grid.mas(r - 1, c - 1, +1, +1) or grid.mas(r + 1, c + 1, -1, -1)):
        return 0

    # Check for /-oriented MAS
    if not (grid.mas(r - 1, c + 1, +1, -1) or grid.mas(r + 1, c - 1, -1, +1)):
        return 0

    return 1


def run(text: str) -> tuple[Any, Any]:
    grid = Grid(text)

    count1 = 0
    count2 = 0

    for r, c in grid:
        count1 += xmas_count(grid, r, c)
        count2 += x_mas_count(grid, r, c)

    return count1, count2
