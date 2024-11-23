import sys
import pathlib
import importlib

_INPUTS = pathlib.Path(__file__).parents[1] / "inputs"


def run(day: int) -> None:
    solver = importlib.import_module(f".day{day:02}", package="aoc")
    data = (_INPUTS / f"{day:02}").read_text()
    solver.run(data)


days = (
    sorted(int(arg) for arg in sys.argv[1:])
    if len(sys.argv) > 1
    else list(range(1, 26))
)
for day in days:
    run(day)
