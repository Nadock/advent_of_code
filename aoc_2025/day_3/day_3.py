def part_1(puzzle: str) -> int | str | float | bool:
    """Solution for AOC 2025, day 3, part 1."""
    banks = puzzle.splitlines()
    total = 0

    for bank in banks:
        max = int(bank[:2])

        for curr in range(len(bank)):
            if int(bank[curr]) < int(str(max)[0]):
                continue

            for next in range(curr + 1, len(bank)):
                value = int(bank[curr] + bank[next])
                if value > max:  # noqa: PLR1730
                    max = value

        total += max

    return total


def part_2(puzzle: str) -> int | str | float | bool:
    """Solution for AOC 2025, day 3, part 2."""
    del puzzle
    return "Part 2 TBD"
