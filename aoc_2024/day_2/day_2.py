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


def part_2(puzzle: str) -> int | str | float | bool:
    """Solution for AOC 2024, day 2, part 2."""
    del puzzle
    return "Part 2 TBD"
