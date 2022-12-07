"""AOC Day 6 started at 2022-12-06T16:08:27.841108+10:30"""


def part1(puzzle: str):
    """Calculates the solution to day 6's first part."""
    buf = puzzle.strip()

    start = -1
    for idx in range(0, len(buf)):
        window = buf[idx : idx + 4]
        if len(set(window)) == 4:
            start = idx + 4
            break

    return start


def part2(puzzle: str):
    """Calculates the solution to day 6's second part."""
    buf = puzzle.strip()

    start = -1
    for idx in range(0, len(buf)):
        window = buf[idx : idx + 14]
        if len(set(window)) == 14:
            start = idx + 14
            break

    return start
