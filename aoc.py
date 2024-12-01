#!/usr/bin/env python
import argparse
import datetime
import importlib
import json
import math
import os
import pathlib
import subprocess
import sys
import time
import webbrowser
from typing import Any, Literal, assert_never

import bs4
import requests
import rich
from requests import utils
from rich import console, table, traceback


def init_argparse() -> argparse.ArgumentParser:
    """Create an argument parser for `aoc.py` CLI usage."""
    today = datetime.datetime.now().astimezone()

    parser = argparse.ArgumentParser(prog="aoc.py")
    parser.add_argument(
        "--session",
        type=pathlib.Path,
        default=pathlib.Path("./cookie.txt"),
        help=(
            "The path to a file containing your AOC session cookie, to authenticate "
            "when automatically downloading puzzle inputs. (default: ./cookie.txt)"
        ),
    )
    parser.add_argument(
        "--results",
        type=pathlib.Path,
        default=pathlib.Path("results.json"),
        help=(
            "A JSON file containing the results of previous runs. Update when using "
            "the 'run' command and used reference in the 'test' command."
        ),
    )

    commands = parser.add_subparsers(dest="command", required=True)

    init = commands.add_parser("init", help="Initialise a day's files.")
    init.add_argument(
        "-y",
        "--year",
        type=int,
        default=today.year,
        help=(
            "The year of the puzzle to initialise. (default: the current "
            f'year, eg: "{today.year}")'
        ),
    )
    init.add_argument(
        "-d",
        "--day",
        type=int,
        default=today.day,
        help=(
            "The day of the puzzle to initialise. (default: the current "
            f'day, eg: "{today.day}")'
        ),
    )
    init.add_argument(
        "--no-download",
        dest="do_day_download",
        default=True,
        action="store_false",
        help="Disable the automated download of the day's puzzle inputs.",
    )
    init.add_argument(
        "--no-files",
        dest="do_day_files",
        default=True,
        action="store_false",
        help="Disable to automated creation of solution code files.",
    )
    init.add_argument(
        "--no-wait",
        dest="do_puzzle_wait",
        default=True,
        action="store_false",
        help="Disable the automatic wait for the puzzle to become available.",
    )
    init.add_argument(
        "--no-git",
        dest="do_git_checkout",
        default=True,
        action="store_false",
        help="Disable automatic git branch creation and commit of generated files.",
    )
    init.add_argument(
        "--no-browser",
        dest="do_open_browser",
        default=True,
        action="store_false",
        help="Disable automatic opening the puzzle in the default browser.",
    )

    run = commands.add_parser("run", help="Run the puzzle solution for a day.")
    run.add_argument(
        "-y",
        "--year",
        type=int,
        default=today.year,
        help=(
            "The year of the puzzle to run. (default: the current "
            f'year, eg: "{today.year}")'
        ),
    )
    run.add_argument(
        "-d",
        "--day",
        type=int,
        default=today.day,
        help=(
            "The day of the puzzle to run. (default: the current "
            f'day, eg: "{today.day}")'
        ),
    )
    run.add_argument(
        "-p",
        "--part",
        type=int,
        default=None,
        choices=[1, 2],
        help="The part of the day's puzzle to run. (default: run both parts)",
    )
    run.add_argument(
        "-i",
        "--input",
        default=None,
        choices=["example", "puzzle"],
        help=(
            "Which input to supply to the puzzle. (default: run both inputs, "
            "example first)"
        ),
    )

    test = commands.add_parser(
        "test", help="Test the puzzle solution against previously recorded results."
    )
    test.add_argument(
        "-y",
        "--year",
        type=int,
        default=None,
        help="The year of the puzzles to test. (default: all years)",
    )
    test.add_argument(
        "-d",
        "--day",
        type=int,
        default=None,
        help="The day of the puzzles to test. (default: all days)",
    )
    test.add_argument(
        "-p",
        "--part",
        type=int,
        default=None,
        choices=[1, 2],
        help="The parts of the puzzles to test. (default: both parts)",
    )
    test.add_argument(
        "-i",
        "--input",
        default=None,
        choices=["example", "puzzle"],
        help="The puzzle input to supply to the puzzles. (default: both inputs)",
    )

    return parser


class AOC:
    """Common data a logic for a single AOC puzzle."""

    def __init__(
        self,
        *,
        year: int,
        day: int,
        cookie: pathlib.Path,
        console: console.Console | None = None,
        results: pathlib.Path | None,
    ) -> None:
        self.year = year
        self.day = day
        self.cookie = cookie
        self._cookie: str | None = None
        self.console = console or rich.get_console()
        self.results = results

    def __str__(self) -> str:
        return f"AOC<{format_aoc_id(self)}>"

    def get_session_cookie(self) -> str:
        """Read the session cookie file, or raise a `ValueError`."""
        if self._cookie is not None:
            return self._cookie

        try:
            return self.cookie.read_text("utf-8").strip()
        except Exception as ex:
            self.cookie.write_text("", encoding="utf-8")
            raise ValueError(
                "Please copy the AOC session cookie from your browser into "
                f"{self.cookie} and then try again.",
            ) from ex

    def aoc_http_get(self, path: str) -> requests.Response:
        """Make a HTTP GET call to the supplied AOC path."""
        path = path if not path.startswith("/") else path[1:]
        url = f"https://adventofcode.com/{path}"
        with self.console.status(f'HTTP GET "{url}"'):
            response = requests.get(
                url,
                cookies=utils.cookiejar_from_dict(
                    {"session": self.get_session_cookie()},
                ),
                timeout=10.0,
                headers={"user-agent": "aoc@rileychase.net"},
            )
        response.raise_for_status()
        return response

    def timedelta_to_puzzle(self) -> datetime.timedelta | None:
        """
        Calculate the timedelta between now and when a the current puzzle will be
        available.

        Returns `None` if the puzzle is already available.
        """
        # Puzzle's are related at Midnight EST (UTC-5) each day in December
        puzzle = datetime.datetime(self.year, 12, self.day, 5, 0, 0, 0, datetime.UTC)
        now = datetime.datetime.now(datetime.UTC)

        if now >= puzzle:
            return None
        return puzzle - now

    def wait_for_puzzle(self) -> None:
        """Wait until the current puzzle becomes available."""
        msg = (
            "Waiting for an additional {} until the "
            f"{format_aoc_id(self)} puzzle is available."
        )

        delta = self.timedelta_to_puzzle()
        with self.console.status(msg.format(delta)) as spin:
            while delta is not None:
                time.sleep(1)
                delta = self.timedelta_to_puzzle()
                spin.update(msg.format(delta))

    def get_example_input(self) -> str:
        """Attempt to parse the puzzle HTML page for the example input."""
        response = self.aoc_http_get(f"{self.year}/day/{self.day}")
        soup = bs4.BeautifulSoup(response.text, features="html.parser")
        return soup.find("pre").find("code").text  # type: ignore[union-attr]

    def get_puzzle_input(self) -> str:
        """Retrieve the test input for the current puzzle."""
        return self.aoc_http_get(f"{self.year}/day/{self.day}/input").text

    def get_puzzle_folder(self) -> pathlib.Path:
        """Get the path of the root folder for the current puzzle's files."""
        return pathlib.Path() / f"aoc_{self.year}" / f"day_{self.day}"

    def scaffold_puzzle_files(self) -> pathlib.Path:
        """Create the Python solution files for the current puzzle."""
        folder = self.get_puzzle_folder()
        folder.mkdir(parents=True, exist_ok=True)

        root_init = folder.parent / "__init__.py"
        if not root_init.is_file():
            root_init.write_text("", encoding="utf-8")

        # Create __init__.py
        init_py = folder / "__init__.py"
        if not init_py.is_file():
            init_py.write_text(
                "\n".join(
                    [
                        f"from .day_{self.day} import part_1, part_2",
                        "",
                        '__all__ = ["part_1", "part_2"]',
                        "",
                    ],
                ),
                encoding="utf-8",
            )

        # Create daily solution file
        day_py = folder / f"day_{self.day}.py"
        if not day_py.is_file():
            day_py.write_text(
                "\n".join(
                    [
                        "def part_1(puzzle: str) -> int | str | float | bool:",
                        f'    """Solution for AOC {self.year}, day {self.day}, part 1."""',  # noqa: E501
                        "    del puzzle",
                        '    return "Part 1 TBD"',
                        "",
                        "",
                        "def part_2(puzzle: str) -> int | str | float | bool:",
                        f'    """Solution for AOC {self.year}, day {self.day}, part 2."""',  # noqa: E501
                        "    del puzzle",
                        '    return "Part 2 TBD"',
                        "",
                    ],
                ),
                encoding="utf-8",
            )
        return day_py

    def scaffold_example_input(self) -> pathlib.Path:
        """
        Download the current puzzle's example input and write it to the example input
        file.
        """
        example = self.get_example_input()
        path = self.get_puzzle_folder() / "example.txt"

        folder = self.get_puzzle_folder()
        folder.mkdir(parents=True, exist_ok=True)

        path.write_text(example, encoding="utf-8")
        return path

    def scaffold_puzzle_input(self) -> pathlib.Path:
        """
        Download the current puzzle's test input and write it to the test input file.
        """
        puzzle = self.get_puzzle_input()
        path = self.get_puzzle_folder() / "puzzle.txt"

        folder = self.get_puzzle_folder()
        folder.mkdir(parents=True, exist_ok=True)

        path.write_text(puzzle, encoding="utf-8")
        return path

    def run_part(
        self,
        part: Literal[1, 2],
        input: Literal["example", "puzzle"],
    ) -> str | int | float | bool | None:
        """Run one part of a puzzle with the specified input file."""
        module = importlib.import_module(
            str(self.get_puzzle_folder()).replace("/", "."),
            f"day_{self.day}",
        )
        solution = getattr(module, f"part_{part}")

        puzzle = self.get_puzzle_folder()
        if input == "example":
            puzzle /= "example.txt"
        elif input == "puzzle":
            puzzle /= "puzzle.txt"
        else:
            assert_never(input)

        puzzle_input = puzzle.read_text("utf-8")
        result = None

        try:
            with self.console.status(
                f"Running {format_aoc_id(self, part=part, input=input)}...",
            ):
                result = solution(puzzle_input)

        except KeyboardInterrupt:
            self.console.print(
                "[bold red]KeyboardInterrupt: Stopping "
                + format_aoc_id(self, part=part, input=input, clean=True)
                + ".[/bold red]\n",
            )
            return None

        except Exception:
            # Suppress frames from aoc.py manually
            tb = traceback.Traceback(show_locals=True)
            for stack in tb.trace.stacks:
                stack.frames = [
                    f for f in stack.frames if not f.filename.endswith("aoc.py")
                ]
            self.console.print(
                "Error while running solution for AOC "
                f"{format_aoc_id(self, part=part, input=input)}.",
            )
            self.console.print(tb)
            self.console.print()
            return None

        if not isinstance(result, int | str | float | bool):
            raise TypeError(
                "Expected puzzle solution to be a int, str, float, or bool - "
                f"not {type(result)}",
            )

        self.update_results_file(part, input, result)
        return result

    def add_to_git(self) -> str:
        """Create a new git branch and commit the generated files."""
        branch = f"aoc-{self.year}-day-{self.day}"
        subprocess.run(
            ["/usr/bin/git", "checkout", "-b", branch],
            text=True,
            check=True,
            capture_output=True,
        )

        subprocess.run(
            ["/usr/bin/git", "add", str(self.get_puzzle_folder().parent)],
            text=True,
            check=True,
            capture_output=True,
        )

        subprocess.run(
            [
                "/usr/bin/git",
                "commit",
                "-m",
                f"Add generated files for AOC {self.year} day {self.day}",
            ],
            text=True,
            check=True,
            capture_output=True,
        )

        return branch

    def update_results_file(
        self,
        part: Literal[1, 2],
        input: Literal["example", "puzzle"],
        result: str | float | bool,
    ) -> None:
        """Update the results file with the output of a run."""
        if not self.results:
            return

        results: dict[str, dict[str, dict[str, dict[str, str | float | bool]]]] = {}
        if self.results.is_file():
            results = json.loads(self.results.read_text("utf-8"))

        year, day, _part = str(self.year), str(self.day), str(part)

        results.setdefault(year, {})
        results[year].setdefault(day, {})
        results[year][day].setdefault(_part, {})
        results[year][day][_part][input] = result

        self.results.write_text(json.dumps(results))


def colour_by_type(value: Any) -> str:  # noqa: ANN401
    """Format a value with `rich` console colouring codes according to it's type."""
    if isinstance(value, str):
        return f'[green]"{value}"[/green]'
    if isinstance(value, (int | float)):
        return f"[blue]{value}[/blue]"
    if isinstance(value, bool):
        return f"[yellow]{value}[/yellow]"
    if isinstance(value, pathlib.Path):
        return f"[purple]{value}[/purple]"
    return str(value)


def format_ns_time(time: int) -> str:
    """Human readable format a `time.time_ns` amount of time."""
    seconds = time / 1_000_000_000
    parts = []

    # Breakpoints in seconds
    minute = 60
    hour = 60 * minute

    hours, minutes = 0, 0
    # Format excess hours
    if seconds >= hour:
        hours = math.floor(seconds / hour)
        seconds -= hour * hours
    parts.append(f"{hours:02d}")

    # Format excess minutes
    if seconds >= minute:
        minutes = math.floor(seconds / minute)
        seconds -= minute * minutes
    parts.append(f"{minutes:02d}")

    # Format remaining seconds
    parts.append(f"{seconds:06.3f}")

    return ":".join(parts)


def format_aoc_id(
    year_or_aoc: int | AOC,
    day: int | None = None,
    part: int | None = None,
    input: str | None = None,
    *,
    clean: bool = False,
) -> str:
    """Format an AOC identifier with `rich` console colouring codes."""
    parts = ["AOC"]

    if isinstance(year_or_aoc, AOC):
        parts.append(str(year_or_aoc.year))
        day = day or year_or_aoc.day
    else:
        parts.append(str(year_or_aoc))

    if day is not None:
        parts.append(str(day))

        if part is not None:
            parts.append(str(part))

            if input is not None:
                parts.append(input.upper())

    puzzle_id = ".".join(parts)
    if clean:
        return puzzle_id
    return f"[bold italic cyan]{puzzle_id}[/bold italic cyan]"


def init_command(
    aoc: AOC,
    *,
    do_day_download: bool = True,
    do_day_files: bool = True,
    do_puzzle_wait: bool = True,
    do_git_checkout: bool = True,
    do_open_browser: bool = True,
) -> list[str]:
    """Initialise the solution files and inputs for the supplied AOC puzzle."""
    t = table.Table(
        "[bold cyan]Task[/bold cyan]",
        "[bold cyan]Path[/bold cyan]",
        title=(
            f"[bold italic cyan]Initialising {format_aoc_id(aoc)}[/bold italic cyan]"
        ),
    )
    lines = []

    if do_day_files:
        path = aoc.scaffold_puzzle_files()
        t.add_row(
            "[italic cyan]Scaffold puzzle files[/italic cyan]",
            colour_by_type(path),
        )
        lines.append(str(path))
    else:
        t.add_row(
            "[italic cyan]Scaffold puzzle files[/italic cyan]",
            "[italic white]Skipped[/italic white]",
        )

    if do_puzzle_wait:
        aoc.wait_for_puzzle()

    if do_open_browser:
        url = f"https://adventofcode.com/{aoc.year}/day/{aoc.day}"
        webbrowser.open(url, new=2, autoraise=True)
        t.add_row(
            "[italic cyan]Open puzzle in browser[/italic cyan]",
            colour_by_type(url),
        )
    else:
        t.add_row(
            "[italic cyan]Open puzzle in browser[/italic cyan]",
            "[italic white]Skipped[/italic white]",
        )

    if do_day_download:
        path = aoc.scaffold_puzzle_input()
        t.add_row(
            "[italic cyan]Scaffold puzzle input[/italic cyan]",
            colour_by_type(path),
        )
        lines.append(str(path))

        path = aoc.scaffold_example_input()
        t.add_row(
            "[italic cyan]Scaffold example input[/italic cyan]",
            colour_by_type(path),
        )
        lines.append(str(path))
    else:
        t.add_row(
            "[italic cyan]Scaffold puzzle input[/italic cyan]",
            "[italic white]Skipped[/italic white]",
        )
        t.add_row(
            "[italic cyan]Scaffold example input[/italic cyan]",
            "[italic white]Skipped[/italic white]",
        )

    if do_git_checkout:
        try:
            t.add_row(
                "[italic cyan]Add new files to git[/italic cyan]",
                colour_by_type(aoc.add_to_git()),
            )
        except subprocess.SubprocessError as ex:
            t.add_row(
                "[italic cyan]Add new files to git[/italic cyan]",
                f"[bold red]{ex}[/bold red]",
            )
    else:
        t.add_row(
            "[italic cyan]Add new files to git[/italic cyan]",
            "[italic white]Skipped[/italic white]",
        )

    aoc.console.print(t)
    return lines


def run_command(aoc: AOC, part: int | None, input: str | None) -> list[str]:
    """Run the parts and inputs for the supplied AOC puzzle."""
    parts: list[Literal[1, 2]] = []
    if part is None:
        parts = [1, 2]
    elif part == 1:
        parts = [1]
    elif part == 2:  # noqa: PLR2004
        parts = [2]
    else:
        raise ValueError(f'Unknown value for part "{part}", expected "1" or "2"')

    inputs: list[Literal["example", "puzzle"]] = []
    if input is None:
        inputs = ["example", "puzzle"]
    elif input == "example":
        inputs = ["example"]
    elif input == "puzzle":
        inputs = ["puzzle"]
    else:
        raise ValueError(
            f'Unknown value for input "{input}", expected "example" or "puzzle"',
        )

    t = table.Table(
        "[bold cyan]ID[/bold cyan]",
        "[bold cyan]Duration[/bold cyan]",
        table.Column("[bold cyan]Result[/bold cyan]", justify="center"),
        title=(f"[italic bold cyan]{format_aoc_id(aoc)} Results[/italic bold cyan]"),
    )
    lines = []
    for p in parts:
        for i in inputs:
            start = time.time_ns()
            result = aoc.run_part(p, i)
            end = time.time_ns()

            duration = format_ns_time(end - start)

            if result is None:
                _result = "[bold red]Error, see traceback above.[/bold red]"
            else:
                _result = colour_by_type(result)

            t.add_row(
                format_aoc_id(aoc, part=p, input=i),
                duration,
                _result,
            )

            lines.append(str(result))

    aoc.console.print(t)
    return lines


def test_command(  # noqa: PLR0912
    results_path: pathlib.Path,
    year: int | None,
    day: int | None,
    part: int | None,
    input: Literal["example", "puzzle"] | None,
) -> list[str]:
    """Re-run each previously recorded puzzle to ensure they still work."""
    results: dict[str, dict[str, dict[str, dict[str, str | float | bool]]]] = {}
    results = json.loads(results_path.read_text("utf-8"))

    t = table.Table(
        "[bold cyan]ID[/bold cyan]",
        "[bold cyan]Duration[/bold cyan]",
        table.Column("[bold cyan]Pass / Fail[/bold cyan]", justify="center"),
        table.Column("[bold cyan]Expected[/bold cyan]", justify="center"),
        table.Column("[bold cyan]Got[/bold cyan]", justify="center"),
        title=("[italic bold cyan]AoC Test Results[/italic bold cyan]"),
    )

    fails = 0

    for _year, days in results.items():
        if year is not None and _year != year:
            continue

        for _day, parts in days.items():
            if day is not None and _day != day:
                continue

            aoc = AOC(
                year=int(_year), day=int(_day), cookie=pathlib.Path(), results=None
            )

            for _part, inputs in parts.items():
                if part is not None and _part != part:
                    continue

                for _input, expected in inputs.items():
                    if input is not None and _input != input:
                        continue

                    if int(_part) not in (1, 2):
                        raise ValueError(
                            f"Unknown puzzle part in results file: {_part}"
                        )

                    if _input not in ("example", "puzzle"):
                        raise ValueError(
                            f"Unknown puzzle input in results file: {_input}"
                        )

                    start = time.time_ns()
                    actual = aoc.run_part(int(_part), _input)  # type: ignore[arg-type]
                    end = time.time_ns()

                    duration = format_ns_time(end - start)

                    pass_fail = "✅" if expected == actual else "❌"
                    if expected != actual:
                        fails += 1

                    if actual is None:
                        actual = "[bold red]Error, see traceback above.[/bold red]"
                    else:
                        actual = colour_by_type(actual)

                    t.add_row(
                        format_aoc_id(int(_year), int(_day), int(_part), _input),
                        duration,
                        pass_fail,
                        colour_by_type(expected),
                        actual,
                    )

    rich.get_console().print(t)

    if fails != 0:
        raise ValueError(f"{fails} AoC test runs failed!")
    return []


def main(console: console.Console) -> list[str]:
    """AOC CLI main function."""
    parser = init_argparse()
    args = parser.parse_args()

    if args.command == "test":
        return test_command(args.results, args.year, args.day, args.part, args.input)

    aoc = AOC(
        year=args.year,
        day=args.day,
        cookie=args.session,
        console=console,
        results=args.results,
    )

    if args.command == "init":
        return init_command(
            aoc,
            do_day_download=args.do_day_download,
            do_day_files=args.do_day_files,
            do_puzzle_wait=args.do_puzzle_wait,
            do_git_checkout=args.do_git_checkout,
            do_open_browser=args.do_open_browser,
        )

    if args.command == "run":
        return run_command(aoc, args.part, args.input)

    aoc.console.print(parser.format_usage())
    aoc.console.print(
        f'Unknown command "{args.command}", try "./aoc.py --help" for more info.',
    )
    return []


if __name__ == "__main__":
    file = None if sys.stdout.isatty() else open(os.devnull, "w")  # noqa: SIM115, PTH123
    _console = console.Console(stderr=True, file=file)

    try:
        lines = main(_console)
        if not sys.stdout.isatty():
            for line in lines:
                print(line, file=sys.stdout)
    except KeyboardInterrupt:
        pass
    except Exception:
        _console.print_exception()
    finally:
        if file:
            file.close()
