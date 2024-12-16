import heapq
from collections import defaultdict
from collections.abc import Container, Iterator, Mapping
from typing import Any


class RowCol:
    r: int
    c: int

    def __init__(self, r: int = 0, c: int = 0) -> None:
        self.r = r
        self.c = c

    def __eq__(self, other: Any) -> bool:
        assert isinstance(other, RowCol)
        return self.r == other.r and self.c == other.c

    def __lt__(self, other: Any) -> bool:
        assert isinstance(other, RowCol)
        return (self.r, self.c) < (other.r, other.c)

    def __hash__(self) -> int:
        return hash((self.r, self.c))

    def __add__(self, other: Any) -> "RowCol":
        assert isinstance(other, RowCol)
        return RowCol(self.r + other.r, self.c + other.c)

    def __sub__(self, other: Any) -> "RowCol":
        assert isinstance(other, RowCol)
        return RowCol(self.r - other.r, self.c - other.c)

    def rotated_clockwise(self) -> "RowCol":
        return RowCol(-self.c, self.r)

    def rotated_anticlockwise(self) -> "RowCol":
        return RowCol(self.c, -self.r)


P = RowCol
V = RowCol


def parse_map(data: str) -> tuple[set[P], P, P]:
    allowed: set[P] = set()
    origin = P()
    target = P()

    for r, row in enumerate(data.splitlines()):
        for c, char in enumerate(row):
            p = P(r, c)
            match char:
                case "#":
                    continue
                case ".":
                    pass
                case "S":
                    origin = p
                case "E":
                    target = p
            allowed.add(p)

    return allowed, origin, target


def possible_forward_steps(
    allowed: Container[P], p0: P, v0: V
) -> Iterator[tuple[P, V, int]]:
    p1 = p0 + v0
    if p1 in allowed:
        yield p1, v0, 1

    v1 = v0.rotated_clockwise()
    if p0 + v1 in allowed:
        yield p0, v1, 1000

    v1 = v0.rotated_anticlockwise()
    if p0 + v1 in allowed:
        yield p0, v1, 1000


def possible_backward_steps(
    history: Container[tuple[P, V]], p0: P, v0: V
) -> Iterator[tuple[P, V, int]]:
    p1 = p0 - v0
    if (p1, v0) in history:
        yield p1, v0, 1

    v1 = v0.rotated_clockwise()
    if (p0, v1) in history:
        yield p0, v1, 1000

    v1 = v0.rotated_anticlockwise()
    if (p0, v1) in history:
        yield p0, v1, 1000


def walk_forwards(
    allowed: Container[P], origin: P, target: P
) -> tuple[int, dict[tuple[P, V], int]]:
    target_score = 0xFFFFFFFF
    scores: defaultdict[tuple[P, V], int] = defaultdict(lambda: 0xFFFFFFFF)
    pending: list[tuple[int, P, V]] = []

    p = origin
    v = V(0, +1)

    scores[p, v] = 0
    heapq.heappush(pending, (0, p, v))

    while pending:
        s, p, v = heapq.heappop(pending)
        if p == target:
            if s < target_score:
                target_score = s
            continue

        for next_p, next_v, step_score in possible_forward_steps(allowed, p, v):
            next_score = scores[p, v] + step_score
            if next_score < scores[next_p, next_v]:
                scores[next_p, next_v] = next_score
                heapq.heappush(pending, (next_score, next_p, next_v))

    return target_score, scores


def walk_backwards(
    scores: Mapping[tuple[P, V], int], best_score: int, origin: P, target: P
) -> int:
    visited: set[P] = set()
    pending: set[tuple[P, V, int]] = {
        (p, v, s) for (p, v), s in scores.items() if p == target and s == best_score
    }

    while pending:
        p, v, s = pending.pop()
        visited.add(p)
        if p == origin:
            continue

        for prev_p, prev_v, step_score in possible_backward_steps(scores, p, v):
            prev_score = s - step_score
            if scores[prev_p, prev_v] == prev_score:
                pending.add((prev_p, prev_v, prev_score))

    return len(visited)


def run(data: str) -> None:
    allowed, origin, target = parse_map(data)

    best_score, scores = walk_forwards(allowed, origin, target)
    best_tiles = walk_backwards(scores, best_score, origin, target)

    print(best_score)
    print(best_tiles)
