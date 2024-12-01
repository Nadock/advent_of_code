"""AOC Day 6 started at 2022-12-06T16:08:27.841108+10:30"""  # noqa: D415


def part_1(puzzle: str):  # noqa: ANN201
    """Calculates the solution to day 6's first part."""
    buf = puzzle.strip()

    start = -1
    for idx in range(len(buf)):
        window = buf[idx : idx + 4]
        if len(set(window)) == 4:  # noqa: PLR2004
            start = idx + 4
            break

    return start


def part_2(puzzle: str):  # noqa: ANN201
    """Calculates the solution to day 6's second part."""
    buf = puzzle.strip()

    start = -1
    for idx in range(len(buf)):
        window = buf[idx : idx + 14]
        if len(set(window)) == 14:  # noqa: PLR2004
            start = idx + 14
            break

    return start
