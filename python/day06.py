Position = complex
Heading = complex
Grid = dict[Position, str]


def parse_map(data: str) -> tuple[Position, Grid]:
    guard = Position()
    grid = Grid()

    for r, row in enumerate(data.splitlines()):
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

    assert False


def is_loop(guard: Position, grid: Grid) -> bool:
    history: set[tuple[Position, Heading]] = set()
    heading = Heading(-1, 0)

    while True:
        state = (guard, heading)
        if state in history:
            return True

        history.add(state)
        candidate = guard + heading

        if candidate not in grid:
            return False

        if grid[candidate] == "#":
            heading = rotate(heading)
        else:
            guard = candidate

    assert False


def run(data: str) -> None:
    guard, grid = parse_map(data)

    visited = find_visited(guard, grid)

    loops = 0
    for p in visited:
        if p == guard:
            continue

        grid[p] = "#"
        if is_loop(guard, grid):
            loops += 1
        grid[p] = "."

    print(len(visited))
    print(loops)
