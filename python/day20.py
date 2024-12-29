import functools
import multiprocessing
from collections.abc import Container, Iterable, Mapping
from typing import Any

Position = complex


def parse_map(text: str) -> tuple[Container[Position], Position, Position]:
    walls = set()
    origin = Position()
    target = Position()

    for r, row in enumerate(text.splitlines()):
        for c, char in enumerate(row):
            p = Position(r, c)
            match char:
                case "#":
                    walls.add(p)
                case "S":
                    origin = p
                case "E":
                    target = p

    return walls, origin, target


def get_neighbours(p: Position) -> Iterable[Position]:
    return [
        p + Position(0, -1),
        p + Position(0, +1),
        p + Position(-1, 0),
        p + Position(+1, 0),
    ]


def cheat_moves(times: int) -> Iterable[tuple[int, Position]]:
    moves: list[tuple[int, Position]] = []

    for n in range(1, 1 + times):
        moves.append((n, Position(0, -n)))
        moves.append((n, Position(0, +n)))
        moves.append((n, Position(-n, 0)))
        moves.append((n, Position(+n, 0)))

    for r in range(1, 1 + times):
        for c in range(1, 1 + times - r):
            moves.append((r + c, Position(r, c)))
            moves.append((r + c, Position(-r, c)))
            moves.append((r + c, Position(r, -c)))
            moves.append((r + c, Position(-r, -c)))

    return moves


def find_path(
    walls: Container[Position], origin: Position, target: Position
) -> Mapping[Position, int]:
    path: dict[Position, int] = {origin: 0}

    p = origin
    t = 0
    while p != target:
        t += 1
        for n in get_neighbours(p):
            if n in walls:
                continue
            if n in path:
                continue
            p = n
            path[p] = t
            break

    return path


def count_above_threshold(
    path: Mapping[Position, int],
    start: Position,
    *,
    cheats: Iterable[tuple[int, Position]],
) -> int:
    count = 0

    for cost, move in cheats:
        p = start + move
        if p not in path:
            continue
        saving = path[start] - path[p] - cost
        if saving >= 100:
            count += 1

    return count


def run(text: str) -> tuple[Any, Any]:
    walls, origin, target = parse_map(text)

    path = find_path(walls, origin, target)

    with multiprocessing.Pool() as pool:
        counts2 = pool.map(
            functools.partial(count_above_threshold, path, cheats=cheat_moves(2)),
            path,
        )
        counts20 = pool.map(
            functools.partial(count_above_threshold, path, cheats=cheat_moves(20)),
            path,
        )

    return sum(counts2), sum(counts20)
