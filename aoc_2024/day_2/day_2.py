import itertools


def part_1(puzzle: str) -> int | str | float | bool:
    """Solution for AOC 2024, day 2, part 1."""
    fails = 0

    for line in puzzle.splitlines():
        report = [int(v) for v in line.split()]
        increasing = None

        for a, b in itertools.pairwise(report):
            if a - b == 0 or abs(a - b) > 3:
                fails += 1
                break
            if increasing is None:
                increasing = a - b > 0
            if increasing and a - b < 0:
                fails += 1
                break
            if not increasing and a - b > 0:
                fails += 1
                break

    return len(puzzle.splitlines()) - fails


def is_bad(report: list[int]) -> bool:
    """Returns `True` if a report is bad according to the puzzle rules."""
    increasing = None
    for a, b in itertools.pairwise(report):
        if increasing is None:
            increasing = a - b > 0
        if a - b == 0 or abs(a - b) > 3:
            return True
        if increasing and a - b < 0:
            return True
        if not increasing and a - b > 0:
            return True
    return False


def part_2(puzzle: str) -> int | str | float | bool:
    """Solution for AOC 2024, day 2, part 2."""
    fails = 0

    for line in puzzle.splitlines():
        report = [int(v) for v in line.split()]
        if is_bad(report):
            bad = True
            for idx in range(len(report)):
                sub_report = report[0:idx] + report[idx + 1 :]
                if not is_bad(sub_report):
                    bad = False
                    break
            if bad:
                fails += 1

    return len(puzzle.splitlines()) - fails
