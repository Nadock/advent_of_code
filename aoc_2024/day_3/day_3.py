import re


def part_1(puzzle: str) -> int | str | float | bool:
    """Solution for AOC 2024, day 3, part 1."""
    pattern = re.compile(r"mul\((?P<a>\d{1,3}),(?P<b>\d{1,3})\)")

    sum = 0
    for match in pattern.finditer(puzzle):
        a, b = match.group("a"), match.group("b")
        sum += int(a) * int(b)

    return sum


def part_2(puzzle: str) -> int | str | float | bool:
    """Solution for AOC 2024, day 3, part 2."""
    pattern = re.compile(r"mul\((?P<a>\d{1,3}),(?P<b>\d{1,3})\)")

    part = None
    next = None

    # Split the puzzle input into everything before and after the first "don't()"
    split = puzzle.split("don't()", 1)
    part = split[0]
    if len(split) == 2:
        next = split[1]

    sum = 0
    while True:
        # Apply all the mul(x,y) in the enabled part
        for match in pattern.finditer(part):
            a, b = match.group("a"), match.group("b")
            sum += int(a) * int(b)

        if not next:
            # If next is None there is nothing left to process
            break

        # Split the remaining input before and after the next "do()"
        split = next.split("do()", 1)
        next = None
        if len(split) != 2:
            # If there is only 1 element in split, all of next is disabled so there is
            # nothing left to process
            break

        # Ignore everything before the next "do()", the split what's left before and
        # after the next "don't()".
        split = split[1].split("don't()", 1)
        part = split[0]
        if len(split) == 2:
            next = split[1]

    return sum
