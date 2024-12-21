import functools
import itertools
from collections import defaultdict
from typing import Any

NUMERIC_KEYPAD = {
    "0": {
        "2": "^",
        "A": ">",
    },
    "1": {
        "2": ">",
        "4": "^",
    },
    "2": {
        "0": "v",
        "1": "<",
        "3": ">",
        "5": "^",
    },
    "3": {
        "2": "<",
        "6": "^",
        "A": "v",
    },
    "4": {
        "1": "v",
        "5": ">",
        "7": "^",
    },
    "5": {
        "2": "v",
        "4": "<",
        "6": ">",
        "8": "^",
    },
    "6": {
        "3": "v",
        "5": "<",
        "9": "^",
    },
    "7": {
        "4": "v",
        "8": ">",
    },
    "8": {
        "5": "v",
        "7": "<",
        "9": ">",
    },
    "9": {
        "6": "v",
        "8": "<",
    },
    "A": {
        "0": "<",
        "3": "^",
    },
}

DIRECTIONAL_KEYPAD = {
    "<": {
        "v": ">",
    },
    "v": {
        "<": "<",
        ">": ">",
        "^": "^",
    },
    ">": {
        "v": "<",
        "A": "^",
    },
    "^": {
        "v": "v",
        "A": ">",
    },
    "A": {
        ">": "v",
        "^": "<",
    },
}

SHORTEST_PATHS: dict[str, dict[str, list[str]]] = {}


def find_shortest_paths(
    keypad: dict[str, dict[str, str]],
    origin: str,
) -> dict[str, list[str]]:
    if origin not in keypad:
        return {}

    paths: defaultdict[str, list[str]] = defaultdict(list)
    paths[origin] = [""]

    lengths = defaultdict(lambda: 0xFFFFFFFF)
    lengths[origin] = 0

    queue = [(origin, "")]
    while queue:
        curr_button, curr_path = queue.pop()

        for next_button, next_move in keypad[curr_button].items():
            next_path = curr_path + next_move

            if len(next_path) > lengths[next_button]:
                continue

            queue.append((next_button, next_path))
            if len(next_path) == lengths[next_button]:
                paths[next_button].append(next_path)
            elif len(next_path) < lengths[next_button]:
                lengths[next_button] = len(next_path)
                paths[next_button] = [next_path]

    return {b: [p + "A" for p in ps] for b, ps in paths.items()}


@functools.cache
def expanded_length(sequence: str, depth: int) -> int:
    length = 0
    for a, b in itertools.pairwise("A" + sequence):
        paths = SHORTEST_PATHS[a][b]
        if depth == 0:
            length += len(paths[0])
        else:
            length += min(expanded_length(p, depth - 1) for p in paths)
    return length


def run(text: str) -> tuple[Any, Any]:
    codes = text.splitlines()

    for button in set(NUMERIC_KEYPAD) | set(DIRECTIONAL_KEYPAD):
        numeric_paths = find_shortest_paths(NUMERIC_KEYPAD, button)
        directional_paths = find_shortest_paths(DIRECTIONAL_KEYPAD, button)
        SHORTEST_PATHS[button] = numeric_paths | directional_paths

    total1 = 0
    total2 = 0
    for code in codes:
        code_num = int(code[:-1])
        total1 += code_num * expanded_length(code, 2)
        total2 += code_num * expanded_length(code, 25)

    return total1, total2
