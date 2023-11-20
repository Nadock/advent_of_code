import pathlib

import pytest

import aoc

_nanosecond = 1
_millisecond = 1_000_000 * _nanosecond
_second = 1_000 * _millisecond
_minute = 60 * _second
_hour = 60 * _minute


@pytest.mark.parametrize(
    ("time", "formatted"),
    [
        (_nanosecond, "00:00:00.000"),
        (_millisecond, "00:00:00.001"),
        (_second, "00:00:01.000"),
        (_minute, "00:01:00.000"),
        (_hour, "01:00:00.000"),
        (100 * _hour, "100:00:00.000"),
        ((4 * _hour) + (3 * _minute) + (2 * _second) + _millisecond, "04:03:02.001"),
    ],
)
def test_format_ns_time(time: int, formatted: str) -> None:
    result = aoc.format_ns_time(time)
    assert result == formatted


@pytest.mark.parametrize(
    ("year_or_aoc", "day", "part", "input", "formatted"),
    [
        (2023, 1, 2, "example", "AOC.2023.1.2.EXAMPLE"),
        (2023, 1, 2, None, "AOC.2023.1.2"),
        (2023, 1, None, None, "AOC.2023.1"),
        (2023, None, None, None, "AOC.2023"),
        (
            aoc.AOC(year=2023, day=1, cookie=pathlib.Path()),
            None,
            None,
            None,
            "AOC.2023.1",
        ),
        (
            aoc.AOC(year=2023, day=1, cookie=pathlib.Path()),
            2,
            None,
            None,
            "AOC.2023.2",
        ),
        (
            aoc.AOC(year=2023, day=1, cookie=pathlib.Path()),
            None,
            2,
            None,
            "AOC.2023.1.2",
        ),
        (
            aoc.AOC(year=2023, day=1, cookie=pathlib.Path()),
            None,
            2,
            "example",
            "AOC.2023.1.2.EXAMPLE",
        ),
    ],
)
def test_format_aoc_id(
    year_or_aoc: int | aoc.AOC,
    day: int | None,
    part: int | None,
    input: str | None,
    formatted: str,
) -> None:
    result = aoc.format_aoc_id(year_or_aoc, day, part, input, clean=True)
    assert result == formatted
