import re
from collections.abc import Iterator


def extract_multiplications(data: str, conditionals: bool) -> Iterator[tuple[int, int]]:
    enabled = True
    for m in re.finditer(r"do\(\)|don\'t\(\)|mul\((\d{1,3}),(\d{0,3})\)", data):
        match m.group(0):
            case "do()":
                if conditionals:
                    enabled = True
            case "don't()":
                if conditionals:
                    enabled = False
            case _:
                if enabled:
                    yield int(m.group(1)), int(m.group(2))


def run(data: str) -> None:
    total_unconditional = sum(
        a * b for a, b in extract_multiplications(data, conditionals=False)
    )
    total_conditional = sum(
        a * b for a, b in extract_multiplications(data, conditionals=True)
    )

    print(total_unconditional)
    print(total_conditional)
