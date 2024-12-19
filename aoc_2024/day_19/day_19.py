import functools


def part_1(puzzle: str) -> int | str | float | bool:
    """Solution for AOC 2024, day 19, part 1."""
    towels = puzzle.splitlines()[0].split(", ")
    patterns = puzzle.splitlines()[2:]

    sum = 0
    for pattern in patterns:
        if find_towel_pattern(towels, pattern):
            sum += 1

    return sum


def find_towel_pattern(towels: list[str], target: str) -> list[str] | None:
    """Find a valid towel pattern."""
    options: list[list[str]] = [[]]

    while options:
        option = options.pop(0)
        current = "".join(option)
        if current == target:
            return option

        remaining = target.removeprefix(current)
        for towel in towels:
            if remaining.startswith(towel):
                options.append([*option, towel])  # noqa: PERF401

        options.sort(key=lambda o: len(o), reverse=True)

    return None


def part_2(puzzle: str) -> int | str | float | bool:
    """Solution for AOC 2024, day 19, part 2."""
    towels = puzzle.splitlines()[0].split(", ")
    patterns = puzzle.splitlines()[2:]

    @functools.cache
    def count_ways(target: str) -> int:
        """Count the number of valid towel arrangements."""
        if target == "":
            return 1

        return sum(
            [
                count_ways(target.removeprefix(towel))
                for towel in towels
                if target.startswith(towel)
            ]
        )

    return sum([count_ways(target) for target in patterns])
