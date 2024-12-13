import re
from collections.abc import Iterator
from typing import NamedTuple


class Point(NamedTuple):
    x: int
    y: int

    @property
    def gradient(self) -> float:
        return self.y / self.x


def extract_claw_machines(data: str) -> Iterator[tuple[Point, Point, Point]]:
    for chunk in data.split("\n\n"):
        a = re.search(r"Button A\: X\+(\d+), Y\+(\d+)", chunk)
        b = re.search(r"Button B\: X\+(\d+), Y\+(\d+)", chunk)
        p = re.search(r"Prize\: X\=(\d+), Y\=(\d+)", chunk)

        assert a is not None
        assert b is not None
        assert p is not None

        yield (
            Point(int(a[1]), int(a[2])),
            Point(int(b[1]), int(b[2])),
            Point(int(p[1]), int(p[2])),
        )


def find_gradient_intercept(p1: Point, p2: Point) -> tuple[float, float]:
    x1, y1 = p1
    x2, y2 = p2

    m = (p2.y - p1.y) / (p2.x - p1.x)
    c = p1.y - m * p1.x

    return m, c


def find_intersection(m1: float, c1: float, m2: float, c2: float) -> Point:
    x = (c2 - c1) / (m1 - m2)
    return Point(round(x), 0)


def fewest_tokens(a: Point, b: Point, p: Point) -> int:
    # Rule out machines where the vectors from both buttons are either too steep
    # or too shallow. There's no combination of moves which can ever lead to the
    # prize.
    if a.gradient > p.gradient and b.gradient > p.gradient:
        return 0
    if a.gradient < p.gradient and b.gradient < p.gradient:
        return 0

    # Consider two rays:
    #
    # 1. Moving outwards from the origin by repeatedly pressing button A
    # 2. Moving backwards from the prize by repeatedly un-pressing button B
    #
    # Having already ruled out machines which cannot possibly reach the prize,
    # for all other machines these two rays must intersect. So long as the
    # intersection occurs at integer coordinates then, by definition, starting
    # from the origin and only pressing button A must reach the intersection,
    # then from the intersection only pressing button B must reach the prize.
    #
    # The goal, then, is to find the coordinates of the intersection, from which
    # the number of presses of each button can be derived. In fact, either the X
    # coordinate or the Y coordinate of the intersection is sufficient for this.

    m1, c1 = find_gradient_intercept(Point(0, 0), a)
    m2, c2 = find_gradient_intercept(p, Point(p.x - b.x, p.y - b.y))
    i = find_intersection(m1, c1, m2, c2)

    # Divide the distance covered along the x-axis to reach the intersection
    # from each end to find the number of button presses required.
    na = i.x // a.x
    nb = (p.x - i.x) // b.x
    if na < 0:
        return 0
    if nb < 0:
        return 0

    # Replay the button presses to confirm they do reach the prize.
    x = na * a.x + nb * b.x
    y = na * a.y + nb * b.y
    if x == p.x and y == p.y:
        return 3 * na + nb
    return 0


def run(data: str) -> None:
    total1 = 0
    total2 = 0

    for a, b, p in extract_claw_machines(data):
        total1 += fewest_tokens(a, b, p)
        total2 += fewest_tokens(a, b, Point(p.x + 10000000000000, p.y + 10000000000000))

    print(total1)
    print(total2)
