import datetime
import pathlib

import freezegun
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
            aoc.AOC(year=2023, day=1, cookie=pathlib.Path(), results=None),
            None,
            None,
            None,
            "AOC.2023.1",
        ),
        (
            aoc.AOC(year=2023, day=1, cookie=pathlib.Path(), results=None),
            2,
            None,
            None,
            "AOC.2023.2",
        ),
        (
            aoc.AOC(year=2023, day=1, cookie=pathlib.Path(), results=None),
            None,
            2,
            None,
            "AOC.2023.1.2",
        ),
        (
            aoc.AOC(year=2023, day=1, cookie=pathlib.Path(), results=None),
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


@freezegun.freeze_time("2023-12-03 05:0:00", tz_offset=0)
@pytest.mark.parametrize(
    ("year", "day", "delta"),
    [
        (2023, 1, None),  # Puzzle before now
        (2023, 3, None),  # Puzzle exactly now
        (2023, 4, datetime.timedelta(days=1)),  # Puzzle +1 day
        (2024, 3, datetime.timedelta(days=366)),  # Puzzle +1 year
    ],
)
def test_aoc__timedelta_to_puzzle(
    year: int,
    day: int,
    delta: datetime.timedelta | None,
) -> None:
    _aoc = aoc.AOC(year=year, day=day, cookie=pathlib.Path(), results=None)

    result = _aoc.timedelta_to_puzzle()

    assert result == delta
