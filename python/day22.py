from collections import defaultdict
from typing import Any


def evolve(secret: int) -> int:
    secret ^= secret * 64
    secret %= 16777216
    secret ^= secret // 32
    secret %= 16777216
    secret ^= secret * 2048
    secret %= 16777216
    return secret


def run(text: str) -> tuple[Any, Any]:
    secrets = [int(line) for line in text.splitlines()]

    total = 0
    bananas: defaultdict[tuple[int, ...], int] = defaultdict(int)

    for secret in secrets:
        prices: list[int] = [secret % 10]
        changes: list[int] = []

        for i in range(2000):
            secret = evolve(secret)
            prices.append(secret % 10)
            changes.append(prices[i + 1] - prices[i])
        total += secret

        visited: set[tuple[int, ...]] = set()
        for i in range(4, len(prices)):
            window = tuple(changes[i - 4 : i])
            if window in visited:
                continue
            visited.add(window)
            bananas[window] += prices[i]

    return total, max(bananas.values())
