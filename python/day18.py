import heapq


class MemorySpace:
    __slots__ = ("size", "origin", "target", "space", "falling")

    size: int
    origin: int
    target: int
    space: set[int]
    falling: list[int]

    def __init__(self, size: int, data: str) -> None:
        self.size = size
        self.origin = 0
        self.target = size * size - 1

        self.space = {x + size * y for x in range(size) for y in range(size)}

        self.falling = []
        for line in reversed(data.splitlines()):
            x, y = line.split(",", maxsplit=1)
            p = int(x) + self.size * int(y)
            self.falling.append(p)

    def corrupt_next_byte(self) -> int:
        p = self.falling.pop()
        self.space.remove(p)
        return p

    def neighbours(self, p: int) -> list[int]:
        y, x = divmod(p, self.size)

        ns = []
        if x > 0:
            ns.append(p - 1)
        if x < self.size - 1:
            ns.append(p + 1)
        if y > 0:
            ns.append(p - self.size)
        if y < self.size - 1:
            ns.append(p + self.size)

        return [n for n in ns if n in self.space]

    def manhattan(self, p: int) -> int:
        y, x = divmod(p, self.size)
        return (self.size - 1 - x) + (self.size - 1 - y)

    def find_shortest_path(self) -> int:
        best = {p: 0xFFFFFFFF for p in self.space}
        best[self.origin] = 0

        pending: list[tuple[int, int]] = []
        heapq.heappush(pending, (0, self.origin))

        while pending:
            _, p = heapq.heappop(pending)
            if p == self.target:
                break

            pcost = best[p]
            for n in self.neighbours(p):
                ncost = pcost + 1
                if ncost < best[n]:
                    best[n] = ncost
                    priority = ncost + self.manhattan(n)
                    heapq.heappush(pending, (priority, n))

        return best[self.target]


def run(data: str) -> None:
    memory_space = MemorySpace(71, data)

    for _ in range(1024):
        _ = memory_space.corrupt_next_byte()
    steps1 = memory_space.find_shortest_path()

    while True:
        p = memory_space.corrupt_next_byte()
        if memory_space.find_shortest_path() == 0xFFFFFFFF:
            y, x = divmod(p, memory_space.size)
            coords = f"{x},{y}"
            break

    print(steps1)
    print(coords)
