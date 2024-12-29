import importlib
import sys
import time
from pathlib import Path

MICROSECONDS = "\u03bcs"
ANSI_ESCAPE = "\u001b"
ANSI_GREEN = f"{ANSI_ESCAPE}[32m"
ANSI_RESET = f"{ANSI_ESCAPE}[0m"

ROOT = Path(__file__).parents[1]


def run(day: int) -> None:
    solver = importlib.import_module(f"day{day:02}")
    input_path = ROOT / "inputs" / f"{day:02}"
    input_text = input_path.read_text()

    start = time.perf_counter_ns()
    solution = solver.run(input_text)
    end = time.perf_counter_ns()

    print(
        f"{ANSI_GREEN}Day {day:02} ({round((end - start) / 1000):_} {MICROSECONDS}){ANSI_RESET}"
    )
    print(solution[0])
    print(solution[1])
    print()


if __name__ == "__main__":
    days_to_run = {int(arg) for arg in sys.argv[1:]}
    for day in range(1, 26):
        if days_to_run and day not in days_to_run:
            continue
        run(day)
