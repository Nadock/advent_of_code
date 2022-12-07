import string

_priorities = dict(zip(string.ascii_letters, range(1, 53)))


def item_priority(item: str) -> int:
    return _priorities[item]


def part1(puzzle: str):
    """Calculates the solution to day 3's first part."""
    count = 0

    for line in puzzle.split("\n"):
        compartment1 = set(line[0 : len(line) // 2])
        compartment2 = set(line[len(line) // 2 :])

        for dupe in list(compartment1.intersection(compartment2)):
            count += item_priority(dupe)

    return count


def part2(puzzle: str):
    """Calculates the solution to day 3's second part."""
    lines = puzzle.strip().split("\n")
    count = 0

    for idx in range(0, len(lines), 3):
        dupe = (
            set(lines[idx])
            .intersection(set(lines[idx + 1]))
            .intersection(set(lines[idx + 2]))
        )
        assert len(dupe) == 1
        count += item_priority(list(dupe)[0])

    return count
