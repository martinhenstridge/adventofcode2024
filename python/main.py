import importlib
import pathlib
import sys
import time


def run(day: int) -> None:
    solver = importlib.import_module(f"day{day:02}")
    input_text = pathlib.Path(f"inputs/{day:02}").read_text()

    start = time.perf_counter_ns()
    solution = solver.run(input_text)
    end = time.perf_counter_ns()

    print(f"{day:02} ({round((end - start) / 1000):_} \u03bcs)")
    print(f":: {solution[0]}")
    print(f":: {solution[1]}")
    print()


if __name__ == "__main__":
    days_to_run = {int(arg) for arg in sys.argv[1:]}
    for day in range(1, 26):
        if days_to_run and day not in days_to_run:
            continue
        run(day)
