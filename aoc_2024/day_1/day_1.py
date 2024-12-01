def part_1(puzzle: str) -> int | str | float | bool:
    """Solution for AOC 2024, day 1, part 1."""
    left, right = [], []
    for line in puzzle.splitlines():
        left.append(int(line.split()[0]))
        right.append(int(line.split()[1]))

    left.sort()
    right.sort()

    sum = 0
    for l, r in zip(left, right, strict=True):
        sum += abs(l - r)

    return sum


def part_2(puzzle: str) -> int | str | float | bool:
    """Solution for AOC 2024, day 1, part 2."""
    left, right = [], []
    for line in puzzle.splitlines():
        left.append(int(line.split()[0]))
        right.append(int(line.split()[1]))

    right_counts: dict[int, int] = {}
    for r in right:
        right_counts.setdefault(r, 0)
        right_counts[r] += 1

    sum = 0
    for l in left:
        sum += l * right_counts.get(l, 0)

    return sum
