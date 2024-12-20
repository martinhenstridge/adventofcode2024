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


def find_cheat_savings(
    path: Mapping[Position, int], threshold: int, moves: Iterable[tuple[int, Position]]
) -> int:
    count = 0

    for p0, t0 in path.items():
        for cost, move in moves:
            p = p0 + move
            if p not in path:
                continue
            saving = t0 - path[p] - cost
            if saving >= threshold:
                count += 1

    return count


def run(text: str) -> tuple[Any, Any]:
    walls, origin, target = parse_map(text)

    path = find_path(walls, origin, target)

    count2 = find_cheat_savings(path, threshold=100, moves=cheat_moves(2))
    count20 = find_cheat_savings(path, threshold=100, moves=cheat_moves(20))

    return count2, count20
