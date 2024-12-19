import importlib
import pathlib
import sys
import time

PROBLEMS = [(f"inputs/{day:02}", f"day{day:02}") for day in range(1, 20)]


days_to_run = {int(arg) for arg in sys.argv[1:]}


for day, (input_path, solver_module) in enumerate(PROBLEMS, 1):
    if days_to_run and day not in days_to_run:
        continue

    input_text = pathlib.Path(input_path).read_text()
    solver = importlib.import_module(solver_module)

    start = time.perf_counter_ns()
    solution = solver.run(input_text)
    end = time.perf_counter_ns()

    print(f"{day:>2}-1 :: {solution[0]}")
    print(f"{day:>2}-2 :: {solution[1]}")
    print(f"time :: {round((end - start) / 1000):_} \u03bcs\n")
