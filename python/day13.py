import re
from collections.abc import Iterator

Pair = tuple[int, int]


def extract_claw_machines(data: str) -> Iterator[tuple[Pair, Pair, Pair]]:
    for chunk in data.split("\n\n"):
        a = re.search(r"Button A\: X\+(\d+), Y\+(\d+)", chunk)
        b = re.search(r"Button B\: X\+(\d+), Y\+(\d+)", chunk)
        p = re.search(r"Prize\: X\=(\d+), Y\=(\d+)", chunk)

        assert a is not None
        assert b is not None
        assert p is not None

        yield (
            (int(a[1]), int(a[2])),
            (int(b[1]), int(b[2])),
            (int(p[1]), int(p[2])),
        )


def find_AB(a: Pair, b: Pair, p: Pair) -> Pair:
    # Given:
    # A.xa + B.xb = xp
    # A.ya + B.yb = yp
    # Rearrange to find A and B.

    B = (a[0] * p[1] - p[0] * a[1]) // (a[0] * b[1] - b[0] * a[1])
    A = (p[0] - B * b[0]) // a[0]

    return A, B


def tokens(a: Pair, b: Pair, p: Pair) -> int:
    A, B = find_AB(a, b, p)

    x = A * a[0] + B * b[0]
    y = A * a[1] + B * b[1]

    if x == p[0] and y == p[1]:
        return 3 * A + B
    return 0


def run(data: str) -> None:
    total1 = 0
    total2 = 0

    for a, b, p in extract_claw_machines(data):
        total1 += tokens(a, b, p)
        total2 += tokens(a, b, (p[0] + 10000000000000, p[1] + 10000000000000))

    print(total1)
    print(total2)
