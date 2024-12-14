from typing import Literal


def part_1(puzzle: str) -> int | str | float | bool:
    """Solution for AOC 2024, day 7, part 1."""
    sum = 0
    for line in puzzle.splitlines():
        target = int(line.split(": ", 1)[0])
        numbers = [int(i) for i in line.split(": ", 1)[1].split()]
        if can_produce_target_part_1(target, numbers):
            sum += target
    return sum


def can_produce_target_part_1(
    target: int, numbers: list[int], next_op: Literal["+", "*"] | None = None
) -> bool:
    """
    Returns true if some combination of `+` or `*` operations can combine `numbers` into
    the `target`.

    `next_op` is for the recursion branching and is not needed for the initial call.
    """
    if len(numbers) == 1:
        return target == numbers[0]
    if numbers[0] > target:
        return False

    if next_op is not None:
        if next_op == "+":
            n = numbers[0] + numbers[1]
        elif next_op == "*":
            n = numbers[0] * numbers[1]
        else:
            raise ValueError(f"{next_op=}")

        numbers = [n, *numbers[2:]]

    return can_produce_target_part_1(target, numbers, "+") or can_produce_target_part_1(
        target, numbers, "*"
    )


def part_2(puzzle: str) -> int | str | float | bool:
    """Solution for AOC 2024, day 7, part 2."""
    sum = 0
    for line in puzzle.splitlines():
        target = int(line.split(": ", 1)[0])
        numbers = [int(i) for i in line.split(": ", 1)[1].split()]
        if can_produce_target_part_2(target, numbers):
            sum += target
    return sum


def can_produce_target_part_2(
    target: int, numbers: list[int], next_op: Literal["+", "*", "||"] | None = None
) -> bool:
    """
    Returns true if some combination of `+`, `*`, or `||` operations can combine
    `numbers` into the `target`.

    `next_op` is for the recursion branching and is not needed for the initial call.

    The `||` operation is string concatenation, i.e. `420 || 69 == 42069`.
    """
    if len(numbers) == 1:
        return target == numbers[0]
    if numbers[0] > target:
        return False

    if next_op is not None:
        if next_op == "+":
            n = numbers[0] + numbers[1]
        elif next_op == "*":
            n = numbers[0] * numbers[1]
        elif next_op == "||":
            n = int(f"{numbers[0]}{numbers[1]}")
        else:
            raise ValueError(f"{next_op=}")

        numbers = [n, *numbers[2:]]

    return (
        can_produce_target_part_2(target, numbers, "+")
        or can_produce_target_part_2(target, numbers, "*")
        or can_produce_target_part_2(target, numbers, "||")
    )
