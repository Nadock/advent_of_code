#!/usr/bin/env python
import argparse
import importlib
import pathlib
import sys

import bs4
import requests
from requests import utils


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


def get_input_for_day(day: int) -> pathlib.Path:
    """
    Attempt to download the input details from the AOC site for a given day.

    This function makes two HTTP requests, the first to the `/input` endpoint for that
    day to retrieve the user-unique puzzle input. This requires a session token in the
    `./session_cookie` file.
    The second request to the the main puzzle page to attempt to extract the example
    input. This is less stable so it is done second, and relies on the example being
    the first `<code>` tag on the page.

    The returned path is the directory containing the two input files.
    """
    input0 = pathlib.Path(f"./src/day{day}/input0.txt").absolute()
    input1 = pathlib.Path(f"./src/day{day}/input1.txt").absolute()
    if not input0.is_file() or not input1.is_file():
        raise OSError(f"One or both input files are missing in {input0.parent}")

    # Read session cookie from disk
    session_cookie = pathlib.Path("./.session_cookie").absolute()
    if not session_cookie.is_file():
        session_cookie.write_text("", "utf-8")
        raise OSError(
            f"Please copy your session cookie from your web browser into {session_cookie}"
        )
    session = session_cookie.read_text("utf-8").strip()

    # Get input 1 from the input endpoint
    input1_resp = requests.get(
        f"https://adventofcode.com/2022/day/{day}/input",
        cookies=utils.cookiejar_from_dict({"session": session}),
        timeout=10.0,
        headers={"user-agent": "aoc@rileychase.net"},
    )
    input1_resp.raise_for_status()
    input1.write_text(input1_resp.text, "utf-8")

    # Get input 0 from the first code block on the puzzle page
    input0_resp = requests.get(
        f"https://adventofcode.com/2022/day/{day}",
        timeout=10.0,
        headers={"user-agent": "aoc@rileychase.net"},
    )
    input0_resp.raise_for_status()
    input0.write_text(
        bs4.BeautifulSoup(input0_resp.text, features="html.parser")
        .find("pre")
        .find("code")
        .text,
        "utf-8",
    )

    return input0.parent


def scaffold_day(day: str) -> pathlib.Path:
    """Scaffold files for a single day's AOC challenge solution code."""
    try:
        day_i = int(day.lower().strip().replace("day", ""))
    except ValueError as ex:
        raise ValueError(f"Unknown AOC day '{day}'") from ex

    folder = pathlib.Path(f"./src/day{day_i}").absolute()
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
    (folder / "__init__.py").write_text("", "utf-8")
    (folder / f"day{day_i}.py").write_text(initial_pycode, "utf-8")
    (folder / "input0.txt").write_text("", "utf-8")
    (folder / "input1.txt").write_text("", "utf-8")

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
        input_i = int(input.lower().strip().replace("input", ""))
    except (ValueError, AttributeError) as ex:
        raise ValueError(f"Unknown AOC puzzle input file '{input}'") from ex

    path = pathlib.Path(f"./src/day{day_i}/input{input_i}.txt").absolute()
    if not path.is_file():
        raise OSError(f"No AOC input file at path: {path}")

    module = importlib.import_module(f"src.day{day_i}.day{day_i}", ".")
    func = getattr(module, f"part{part_i}", None)
    if not func:
        raise ValueError(f"Unable to find function part{part_i} in day{day_i} module")

    return func(path)


if __name__ == "__main__":
    args = _argparse()
    if args.new_day is not None:
        p1 = scaffold_day(args.new_day)
        print(f"Scaffolded day {args.new_day} files...", file=sys.stderr)

        p2 = get_input_for_day(args.new_day)
        print(f"Retrieved puzzle inputs for day {args.new_day}...", file=sys.stderr)

        if p1 != p2:
            raise OSError(
                "Something fucking weird happened and the scaffolded files ended up in "
                f"{p1} but the puzzle inputs ended up in {p2}"
            )
        print(f"Day {args.new_day} is ready to be solved in:", file=sys.stderr)
        print(p1)
    else:
        print(
            f"Solution for day {args.day}, part {args.part}, input {args.input}:",
            file=sys.stderr,
        )
        print(run(args.day, args.part, args.input))
