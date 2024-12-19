from typing import Any


def extract_grid_robot(text: str) -> tuple[dict[complex, str], complex]:
    grid: dict[complex, str] = {}
    robot = complex()

    for r, row in enumerate(text.splitlines()):
        for c, char in enumerate(row):
            p = complex(r, c)
            match char:
                case ".":
                    continue
                case "@":
                    robot = p
                case _:
                    grid[p] = char

    return grid, robot


def extract_moves(text: str) -> list[complex]:
    moves: list[complex] = []

    for char in text:
        match char:
            case "^":
                moves.append(complex(-1, 0))
            case "v":
                moves.append(complex(+1, 0))
            case "<":
                moves.append(complex(0, -1))
            case ">":
                moves.append(complex(0, +1))
            case _:
                continue

    return moves


def draw(grid: dict[complex, str], robot: complex) -> None:
    rlim = int(max(p.real for p in grid))
    clim = int(max(p.imag for p in grid))

    for r in range(rlim + 1):
        for c in range(clim + 1):
            p = complex(r, c)
            if p == robot:
                print("@", end="")
            elif p not in grid:
                print(".", end="")
            else:
                print(grid[p], end="")
        print()


def can_move_boxes(
    grid: dict[complex, str], robot: complex, move: complex
) -> tuple[bool, dict[complex, str]]:
    boxes = {}
    front = {robot}
    seen = set()

    while front:
        p = front.pop() + move

        if p in seen:
            continue

        if p not in grid:
            continue

        match grid[p]:
            case "#":
                return False, {}
            case "O":
                front.add(p)
                boxes[p] = "O"
            case "[":
                q = p + complex(0, +1)
                front.add(p)
                front.add(q)
                boxes[p] = "["
                boxes[q] = "]"
            case "]":
                q = p + complex(0, -1)
                front.add(p)
                front.add(q)
                boxes[p] = "]"
                boxes[q] = "["

        seen |= front

    return True, boxes


def move_boxes(
    grid: dict[complex, str], boxes: dict[complex, str], move: complex
) -> None:
    for p in boxes.keys():
        del grid[p]
    for p, box in boxes.items():
        grid[p + move] = box


def move_robot(grid: dict[complex, str], robot: complex, move: complex) -> complex:
    after = robot + move

    # Updated position is empty, move there
    if after not in grid:
        return after

    # Updated position is wall, no move
    if grid[after] == "#":
        return robot

    # Updated position is a box, find next non-box position in same direction
    can_move, boxes = can_move_boxes(grid, robot, move)

    if not can_move:
        return robot

    move_boxes(grid, boxes, move)
    return after


def calculate_gps(grid: dict[complex, str]) -> int:
    total = 0
    for p, char in grid.items():
        if char in "O[":
            total += 100 * int(p.real) + int(p.imag)
    return total


def run(text: str) -> tuple[Any, Any]:
    grid_text, move_text = text.split("\n\n", maxsplit=1)
    moves = extract_moves(move_text)

    grid, robot = extract_grid_robot(grid_text)
    for move in moves:
        robot = move_robot(grid, robot, move)
    gps_small = calculate_gps(grid)

    grid, robot = extract_grid_robot(
        grid_text.replace("#", "##")
        .replace("O", "[]")
        .replace(".", "..")
        .replace("@", "@.")
    )
    for move in moves:
        robot = move_robot(grid, robot, move)
    gps_large = calculate_gps(grid)

    return gps_small, gps_large
