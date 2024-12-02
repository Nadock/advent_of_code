"""AOC Day 13 started at 2022-12-13T15:32:27.551688+10:30"""  # noqa: D415
# pylint: disable=eval-used

import functools


def part_1(puzzle: str):  # noqa: ANN201
    """Calculates the solution to day 13's first part."""
    count = []
    for idx, pairs in enumerate(puzzle.split("\n\n")):
        assert len(pairs.splitlines()) == 2  # noqa: S101

        pair = (eval(pairs.splitlines()[0]), eval(pairs.splitlines()[1]))  # noqa: S307
        result = compare(pair[0], pair[1])

        if result:
            count.append(idx + 1)

    return sum(count)


def compare(  # noqa: D103, PLR0911
    left: int | list[int],
    right: int | list[int],
) -> bool | None:
    if isinstance(left, int) and isinstance(right, int):
        if left == right:
            return None
        return left < right

    if not isinstance(left, list):
        return compare([left], right)
    if not isinstance(right, list):
        return compare(left, [right])

    for idx in range(max(len(left), len(right))):
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


def part_2(puzzle: str):  # noqa: ANN201
    """Calculates the solution to day 13's second part."""
    packets = [[[2]], [[6]]]
    for line in puzzle.splitlines():
        if not line:
            continue
        packets.append(eval(line))  # noqa: S307

    def sort_compare(left, right) -> int:  # noqa: ANN001
        result = compare(left, right)
        if result:
            return -1
        return 1

    packets = sorted(packets, key=functools.cmp_to_key(sort_compare))

    return (packets.index([[2]]) + 1) * (packets.index([[6]]) + 1)
