import functools


def extract_stones(data: str) -> list[int]:
    return [int(n) for n in data.split()]


def evolve_once(stone: int) -> list[int]:
    if stone == 0:
        return [1]

    digits = str(stone)
    length = len(digits)
    if length % 2 == 0:
        return [int(digits[: length // 2]), int(digits[length // 2 :])]

    return [stone * 2024]


@functools.cache
def evolve(stone: int, generations: int) -> int:
    if generations == 0:
        return 1

    return sum(evolve(st, generations - 1) for st in evolve_once(stone))


def run(data: str) -> None:
    stones = extract_stones(data)

    count1 = sum(evolve(st, generations=25) for st in stones)
    count2 = sum(evolve(st, generations=75) for st in stones)

    print(count1)
    print(count2)
