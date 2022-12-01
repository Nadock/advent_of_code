#!/usr/bin/env python
import argparse
import importlib
import pathlib
import sys


def _argparse() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run an Advent of Code 2022 challenge")
    parser.add_argument(
        "day",
        help="The day of the advent calendar to run, eg: 'day1' or '1'.",
        nargs="?",
    )
    parser.add_argument(
        "part",
        help="Which part for this day to run, eg: '1' or '2'.",
        nargs="?",
    )
    parser.add_argument(
        "input",
        help="The name of the input file to solve, eg: 'input0' or '0'.",
        nargs="?",
    )

    parser.add_argument(
        "--new-day",
        "-n",
        help="Scaffold files for a new day's challenge.",
        metavar="DAY",
        default=None,
    )

    return parser.parse_args()


def scaffold_day(day: str) -> pathlib.Path:
    """Scaffold files for a single day's AOC challenge solution code."""
    try:
        day_i = int(day.lower().strip().replace("day", ""))
    except ValueError as ex:
        raise ValueError(f"Unknown AOC day '{day}'") from ex

    folder = pathlib.Path(f"./day{day_i}").absolute()
    if folder.exists():
        raise OSError(f"Folder for day {day_i} already exists: {folder}")

    initial_pycode = "\n".join(
        [
            "import pathlib",
            "",
            "",
            "def part1(path: pathlib.Path):",
            f'    """Calculates the solution to day {day_i}\'s first part."""',
            "",
            "",
            "def part2(path: pathlib.Path):",
            f'    """Calculates the solution to day {day_i}\'s second part."""',
            "",
        ]
    )

    folder.mkdir(parents=True, exist_ok=False)
    (folder / "__init__.py").write_text("")
    (folder / f"day{day_i}.py").write_text(initial_pycode)
    (folder / "input0.txt").write_text("")
    (folder / "input1.txt").write_text("")

    return folder


def run(day: str, part: str, input: str):  # pylint: disable=redefined-builtin
    """
    Load and run the AOC challenge solution code for a given `day`, `part`, & `input`.
    """
    try:
        day_i = int(day.lower().strip().replace("day", ""))
    except (ValueError, AttributeError) as ex:
        raise ValueError(f"Unknown AOC day '{day}'") from ex

    try:
        part_i = int(part.lower().strip().replace("part", ""))
    except (ValueError, AttributeError) as ex:
        raise ValueError(f"Unknown AOC part '{part}'") from ex

    try:
        input_i = int(part.lower().strip().replace("input", ""))
    except (ValueError, AttributeError) as ex:
        raise ValueError(f"Unknown AOC puzzle input file '{input}'") from ex

    path = pathlib.Path(f"./day{day_i}/input{input_i}.txt").absolute()
    if not path.is_file():
        raise OSError(f"No AOC input file at path: {path}")

    module = importlib.import_module(f"day{day_i}.day{day_i}", "2022")
    func = getattr(module, f"part{part_i}", None)
    if not func:
        raise ValueError(f"Unable to find function part{part_i} in day{day_i} module")

    return func(path)


if __name__ == "__main__":
    args = _argparse()
    if args.new_day is not None:
        print("Scaffolded new day in", scaffold_day(args.new_day), file=sys.stderr)
    else:
        print(
            f"Solution for day {args.day}, part {args.part}, input {args.input}:",
            run(args.day, args.part, args.input),
            file=sys.stderr,
        )
