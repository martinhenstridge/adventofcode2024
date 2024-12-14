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
    ("inputs/05", "day05"),
    ("inputs/06", "day06"),
    ("inputs/07", "day07"),
    ("inputs/08", "day08"),
    ("inputs/09", "day09"),
    ("inputs/10", "day10"),
    ("inputs/11", "day11"),
    ("inputs/12", "day12"),
    ("inputs/13", "day13"),
    ("inputs/14", "day14"),
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
    duration = (end - start) * 1e-9
    print(f"======\nt (s) = {duration:.2e}")
    print()
