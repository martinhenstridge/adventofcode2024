from typing import Any


def run(text: str) -> tuple[Any, Any]:
    locks: list[list[int]] = []
    keys: list[list[int]] = []

    for chunk in text.split("\n\n"):
        rows = chunk.splitlines()
        cols = zip(*rows)

        heights = [col.count("#") - 1 for col in cols]
        if chunk.startswith("#"):
            locks.append(heights)
        else:
            keys.append(heights)

    fit_count = sum(
        1 if all(pins + teeth < 6 for pins, teeth in zip(lock, key)) else 0
        for lock in locks
        for key in keys
    )

    return fit_count, None
