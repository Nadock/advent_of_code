"""AOC Day 6 started at 2022-12-06T16:08:27.841108+10:30"""

import pathlib


def part1(path: pathlib.Path):
    """Calculates the solution to day 6's first part."""
    buf = path.read_text("utf-8").strip()

    start = -1
    for idx in range(0, len(buf)):
        window = buf[idx : idx + 4]
        if len(set(window)) == 4:
            start = idx + 4
            break

    return start


def part2(path: pathlib.Path):
    """Calculates the solution to day 6's second part."""
    buf = path.read_text("utf-8").strip()

    start = -1
    for idx in range(0, len(buf)):
        window = buf[idx : idx + 14]
        if len(set(window)) == 14:
            start = idx + 14
            break

    return start
