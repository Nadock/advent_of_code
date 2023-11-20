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
