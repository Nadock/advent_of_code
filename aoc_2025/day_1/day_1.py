def part_1(puzzle: str) -> int | str | float | bool:
    """Solution for AOC 2025, day 1, part 1."""
    dial = 50
    count = 0

    for line in puzzle.splitlines():
        dir = line.strip()[0]
        amount = int(line.strip()[1:]) % 100

        if dir == "R":
            dial = (dial + amount) % 100
        elif dir == "L":
            dial = (dial - amount) % 100

        if dial == 0:
            count += 1

    return count


def part_2(puzzle: str) -> int | str | float | bool:
    """Solution for AOC 2025, day 1, part 2."""
    dial = 50
    count = 0

    for line in puzzle.splitlines():
        dir = line.strip()[0]
        amount = int(line.strip()[1:]) % 100
        full_rot = int(line.strip()[1:]) // 100

        if dir == "R":
            full_rot += (dial + amount) // 100
            dial = (dial + amount) % 100
        elif dir == "L":
            full_rot -= (dial - amount) // 100
            dial = (dial - amount) % 100

        count += full_rot

    return count
