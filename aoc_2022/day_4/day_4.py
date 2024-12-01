def part_1(puzzle: str):  # noqa: ANN201
    """Calculates the solution to day 4's first part."""
    count = 0

    for line in puzzle.strip().split("\n"):
        range1 = [int(i) for i in line.split(",")[0].split("-")]
        range2 = [int(i) for i in line.split(",")[1].split("-")]

        if range_full_overlap(range1, range2) or range_full_overlap(range2, range1):
            count += 1

    return count


def range_full_overlap(range1: list[int], range2: list[int]) -> bool:  # noqa: D103
    if range1[0] >= range2[0] and range1[1] <= range2[1]:  # noqa: SIM103
        return True
    return False


def part_2(puzzle: str):  # noqa: ANN201
    """Calculates the solution to day 4's second part."""
    count = 0

    for line in puzzle.strip().split("\n"):
        range1 = [int(i) for i in line.split(",")[0].split("-")]
        range2 = [int(i) for i in line.split(",")[1].split("-")]

        if range_partial_overlap(range1, range2):
            count += 1

    return count


def range_partial_overlap(range1: list[int], range2: list[int]) -> bool:  # noqa: D103
    # Big time cheat here IMO but my brain could not be arsed
    return bool(
        set(range(range1[0], range1[1] + 1)).intersection(
            range(range2[0], range2[1] + 1),
        ),
    )
