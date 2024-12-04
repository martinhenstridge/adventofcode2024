import importlib
import pathlib
import sys
import time


PROBLEMS = [
    ("inputs/00", "day00"),
    ("inputs/01", "day01"),
    ("inputs/02", "day02"),
    ("inputs/03", "day03"),
    ("inputs/04", "day04"),
]


days_to_run = {int(arg) for arg in sys.argv[1:]}


for day, (input_path, solver_module) in enumerate(PROBLEMS[1:], 1):
    if days_to_run and day not in days_to_run:
        continue

    input = pathlib.Path(input_path).read_text()
    solver = importlib.import_module(solver_module)

    print(f"Day {day:02}\n======")
    start = time.perf_counter_ns()
    solver.run(input)
    end = time.perf_counter_ns()
    print(f"======\nt (ns) = {end - start:_}")
    print()
