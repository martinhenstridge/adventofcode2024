import sys
import pathlib
import importlib


_ROOT = pathlib.Path(__file__).parent


if len(sys.argv) > 1:
    days = {int(arg) for arg in sys.argv[1:]}
else:
    days = {
        int(day_py.name.removesuffix(".py").removeprefix("day"))
        for day_py in _ROOT.glob("day*.py")
    }


for num in sorted(days):
    digits = f"{num:02}"
    solver = importlib.import_module(f".day{digits}", package="pyaoc")
    input = (_ROOT.parent / "inputs" / digits).read_text()
    solver.run(input)
