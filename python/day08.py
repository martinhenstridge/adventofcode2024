import itertools
import math
from collections import defaultdict
from collections.abc import Mapping
from typing import Any


def parse_grid(text: str) -> tuple[int, Mapping[str, list[complex]]]:
    antennas: defaultdict[str, list[complex]] = defaultdict(list)

    lines = text.splitlines()
    for r, row in enumerate(lines):
        for c, char in enumerate(row):
            if char == ".":
                continue
            p = complex(r, c)
            antennas[char].append(p)

    return len(lines), antennas


def in_bounds(size: int, p: complex) -> bool:
    return (0 <= p.real < size) and (0 <= p.imag < size)


def find_antinodes_twice(size: int, antennas: list[complex]) -> set[complex]:
    antinodes: set[complex] = set()

    for a, b in itertools.combinations(antennas, 2):
        v = b - a
        if in_bounds(size, antinode := a - v):
            antinodes.add(antinode)
        if in_bounds(size, antinode := b + v):
            antinodes.add(antinode)

    return antinodes


def find_antinodes_harmonic(size: int, antennas: list[complex]) -> set[complex]:
    antinodes: set[complex] = set()

    for a, b in itertools.combinations(antennas, 2):
        v = b - a

        # Verify that the vector between the pair of antennas cannot be reduced
        # (e.g. [2,2] -> [1,1]) such that no antinodes occur in between them and
        # the stride between antinodes beyond them is simply that vector.
        assert math.gcd(int(v.real), int(v.imag)) == 1

        antinode = a
        while in_bounds(size, antinode):
            antinodes.add(antinode)
            antinode -= v

        antinode = b
        while in_bounds(size, antinode):
            antinodes.add(antinode)
            antinode += v

    return antinodes


def run(text: str) -> tuple[Any, Any]:
    size, antennas = parse_grid(text)

    antinodes1: set[complex] = set()
    for positions in antennas.values():
        antinodes1 |= find_antinodes_twice(size, positions)

    antinodes2: set[complex] = set()
    for positions in antennas.values():
        antinodes2 |= find_antinodes_harmonic(size, positions)

    return len(antinodes1), len(antinodes2)
