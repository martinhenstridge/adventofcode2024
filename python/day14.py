import re

Pair = tuple[int, int]


def extract_robots(data: str) -> tuple[list[Pair], list[Pair]]:
    ps: list[Pair] = []
    vs: list[Pair] = []

    for line in data.splitlines():
        match = re.fullmatch(r"p=(\d+),(\d+) v=(\-?\d+),(\-?\d+)", line)
        assert match is not None
        ps.append((int(match[1]), int(match[2])))
        vs.append((int(match[3]), int(match[4])))

    return ps, vs


def move_robots(
    ps: list[Pair], vs: list[Pair], xlim: int, ylim: int, steps: int
) -> list[Pair]:
    p_next = []
    for (px, py), (vx, vy) in zip(ps, vs):
        px += vx * steps
        py += vy * steps
        p_next.append((px % xlim, py % ylim))
    return p_next


def calculate_safety_factor(ps: list[Pair], xlim: int, ylim: int) -> int:
    xmid = xlim // 2
    ymid = ylim // 2

    quadrants = [0, 0, 0, 0]

    for px, py in ps:
        if px < xmid and py < ymid:
            quadrants[0] += 1
        if px > xmid and py < ymid:
            quadrants[1] += 1
        if px < xmid and py > ymid:
            quadrants[2] += 1
        if px > xmid and py > ymid:
            quadrants[3] += 1

    return quadrants[0] * quadrants[1] * quadrants[2] * quadrants[3]


def display(ps: list[Pair], xlim: int, ylim: int, steps: int) -> None:
    grid = [["." for x in range(xlim)] for y in range(ylim)]
    for px, py in ps:
        grid[py][px] = "#"
    for row in grid:
        for char in row:
            print(char, end="")
        print()
    print("t =", steps)


def find_coincidence(a_first: int, a_period: int, b_first: int, b_period: int) -> int:
    t = a_first
    while t % b_period != b_first:
        t += a_period
    return t


def run(data: str) -> None:
    xlim = 101
    ylim = 103

    p0, vs = extract_robots(data)
    p100 = move_robots(p0, vs, xlim, ylim, steps=100)
    safety_factor = calculate_safety_factor(p100, xlim, ylim)

    # From observation there are two cycles in the output where robots cluster
    # together. One is a roughly vertical, the other is roughly horizontal. The
    # hypothesis is that when these two cycles coincide a christmas tree will be
    # displayed.
    #
    # 1. First appearance: 72, period: 103
    # 2. First appearance: 93, period: 101
    #
    # The first coincidence of these sequences can be found by an exhaustive
    # search starting at the first appearance of the first sequence and skipping
    # ahead an entire period at a time until we arrive at a timestep which is
    # also part of the second sequence.
    tree_appearance = find_coincidence(72, 103, 93, 101)

    print(safety_factor)
    print(tree_appearance)
