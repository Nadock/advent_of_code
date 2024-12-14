import functools


def part_1(puzzle: str) -> int | str | float | bool:
    """Solution for AOC 2024, day 11, part 1."""
    stones = [int(s) for s in puzzle.strip().split()]
    return sum([blink(s, 25) for s in stones])


def part_2(puzzle: str) -> int | str | float | bool:
    """Solution for AOC 2024, day 11, part 2."""
    stones = [int(s) for s in puzzle.strip().split()]
    return sum([blink(s, 75) for s in stones])


@functools.cache
def blink(stone: int, blinks: int) -> int:
    """Apply the blink rules to a single stone `blinks` times."""
    if blinks == 0:
        return 1
    if stone == 0:
        return blink(1, blinks - 1)
    if len(s_stone := str(stone)) % 2 == 0:
        left, right = (
            "".join(s_stone[: len(s_stone) // 2]),
            "".join(s_stone[len(s_stone) // 2 :]),
        )
        return blink(int(left), blinks - 1) + blink(int(right), blinks - 1)
    return blink(stone * 2024, blinks - 1)
