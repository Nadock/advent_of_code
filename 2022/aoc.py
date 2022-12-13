#!/usr/bin/env python
import argparse
import dataclasses
import datetime
import importlib
import json
import pathlib
import sys
import time
import traceback
import zoneinfo
from typing import Any, Optional

import bs4
import requests
from requests import utils


@dataclasses.dataclass
class Result:
    value: Any
    exec_time: int
    error: Optional[Exception] = None

    def humanise_exec_time(self) -> str:
        if self.exec_time / 1_000_000_000 > 1:
            return f"{self.exec_time / 1_000_000_000}s"
        return f"{self.exec_time / 1_000_000}ms"


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
    parser.add_argument(
        "--history",
        help="The path to the history file to record execution history in.",
        metavar="PATH",
        default=".aoc_history.json",
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

    now = datetime.datetime.now(zoneinfo.ZoneInfo("Australia/Adelaide"))
    initial_pycode = "\n".join(
        [
            f'"""AOC Day {day_i} started at {now.isoformat()}"""',
            "",
            "",
            "def part1(puzzle: str):",
            f'    """Calculates the solution to day {day_i}\'s first part."""',
            "",
            "",
            "def part2(puzzle: str):",
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


def run(day: str, part: str, input: str) -> Result:  # pylint: disable=redefined-builtin
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
    text = path.read_text("utf-8")

    module = importlib.import_module(f"src.day{day_i}.day{day_i}", ".")
    func = getattr(module, f"part{part_i}", None)
    if not func:
        raise ValueError(f"Unable to find function part{part_i} in day{day_i} module")

    result = None
    err = None

    t_0 = time.time_ns()
    try:
        result = func(text)
    except Exception as ex:  # pylint:disable=broad-except
        err = ex
    t_1 = time.time_ns()

    return Result(value=result, exec_time=t_1 - t_0, error=err)


def _print_result(args: argparse.Namespace, result: Result) -> None:
    if result.error is None:
        print(
            (
                f"Day {args.day}, part {args.part}, input "
                f"{args.input} completed in {result.humanise_exec_time()}:\n"
            ),
            file=sys.stderr,
        )
        print(result.value)
    else:
        print(
            (
                f"Solution for day {args.day}, part {args.part}, input "
                f"{args.input} encountered an error after {result.humanise_exec_time()}:\n"
            ),
            file=sys.stderr,
        )
        traceback.print_exception(
            type(result.error), result.error, result.error.__traceback__
        )


def _store_result(args: argparse.Namespace, result: Result) -> None:
    history = _load_history(args)
    history.setdefault("2022", {})
    history["2022"].setdefault(args.day, {})
    history["2022"][args.day].setdefault(args.part, {})
    history["2022"][args.day][args.part].setdefault(args.input, {})

    history["2022"][args.day][args.part][args.input]["last_run"] = {
        "exec_time": result.exec_time,
        "timestamp": (
            datetime.datetime.now(zoneinfo.ZoneInfo("Australia/Adelaide")).isoformat()
        ),
        "result": result.value,
        "error": str(result.error) if result.error is not None else None,
    }

    pathlib.Path(args.history).write_text(json.dumps(history, indent=2), "utf-8")


def _load_history(args: argparse.Namespace) -> dict:
    history_path = pathlib.Path(args.history).absolute()
    if history_path.exists() and not history_path.is_file():
        raise OSError(f"History file exists but is not a file: {history_path}")
    if not history_path.exists():
        history_path.write_text("{}", "utf-8")
    return json.loads(history_path.read_text("utf-8"))


def main():
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
        result = run(args.day, args.part, args.input)
        _print_result(args, result)
        _store_result(args, result)


if __name__ == "__main__":
    main()
