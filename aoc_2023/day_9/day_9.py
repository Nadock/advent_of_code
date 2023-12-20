import itertools


def part_1(puzzle: str) -> int | str | float | bool:
    """Solution for AOC 2023, day 9, part 1."""
    histories = [[int(num) for num in line.split()] for line in puzzle.splitlines()]

    count = 0
    for history in histories:
        count += extrapolate_forward(history)

    return count


def reduce_history(history: list[int]) -> list[list[int]]:
    reduced_history = [history]
    while not all(h == 0 for h in history):
        history = [b - a for a, b in itertools.pairwise(history)]
        reduced_history.append(history)
    return reduced_history


def extrapolate_forward(history: list[int]) -> int:
    reduced_history = reduce_history(history)
    last_values = [h[-1] for h in reduced_history]

    next = 0
    for current_value in last_values[::-1]:
        next = current_value + next

    return next


def extrapolate_backwards(history: list[int]) -> int:
    reduced_history = reduce_history(history)
    first_values = [h[0] for h in reduced_history]

    next = 0
    for current_value in first_values[::-1]:
        next = current_value - next

    return next


def part_2(puzzle: str) -> int | str | float | bool:
    """Solution for AOC 2023, day 9, part 2."""
    histories = [[int(num) for num in line.split()] for line in puzzle.splitlines()]

    count = 0
    for history in histories:
        count += extrapolate_backwards(history)

    return count
