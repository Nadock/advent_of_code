"""AOC Day 13 started at 2022-12-13T15:32:27.551688+10:30"""
# pylint: disable=eval-used

import functools
from typing import Optional, Union


def part1(puzzle: str):
    """Calculates the solution to day 13's first part."""
    count = []
    for idx, pairs in enumerate(puzzle.split("\n\n")):
        assert len(pairs.splitlines()) == 2

        pair = (eval(pairs.splitlines()[0]), eval(pairs.splitlines()[1]))
        result = compare(pair[0], pair[1])

        if result:
            count.append(idx + 1)

    return sum(count)


def compare(
    left: Union[int, list[int]], right: Union[int, list[int]]
) -> Optional[bool]:

    if isinstance(left, int) and isinstance(right, int):
        if left == right:
            return None
        return left < right

    if not isinstance(left, list):
        return compare([left], right)
    if not isinstance(right, list):
        return compare(left, [right])

    for idx in range(0, max(len(left), len(right))):
        try:
            right_v = right[idx]
        except IndexError:
            return False

        try:
            left_v = left[idx]
        except IndexError:
            return True

        cmp = compare(left_v, right_v)
        if cmp is None:
            continue
        return cmp

    return None


def part2(puzzle: str):
    """Calculates the solution to day 13's second part."""

    packets = [[[2]], [[6]]]
    for line in puzzle.splitlines():
        if not line:
            continue
        packets.append(eval(line))

    def sort_compare(left, right) -> int:
        result = compare(left, right)
        if result:
            return -1
        return 1

    packets = sorted(packets, key=functools.cmp_to_key(sort_compare))

    return (packets.index([[2]]) + 1) * (packets.index([[6]]) + 1)
