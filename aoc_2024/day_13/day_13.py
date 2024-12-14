import functools
import itertools


def part_1(puzzle: str) -> int | str | float | bool:
    """Solution for AOC 2024, day 13, part 1."""
    sum = 0
    for config in itertools.batched(puzzle.splitlines(), 4):
        a = config[0][12:].split(", ", 1)
        a[1] = a[1].removeprefix("Y+")

        b = config[1][12:].split(", ", 1)
        b[1] = b[1].removeprefix("Y+")

        p = config[2][9:].split(", ", 1)
        p[1] = p[1].removeprefix("Y=")

        min_path = search_prize_graph(
            (int(a[0]), int(a[1])),
            (int(b[0]), int(b[1])),
            (int(p[0]), int(p[1])),
        )
        if min_path:
            sum += min_path

    return sum


@functools.cache
def search_prize_graph(
    a: tuple[int, int],
    b: tuple[int, int],
    target: tuple[int, int],
    current: tuple[int, int] = (0, 0),
    path_len: int = 0,
) -> int | None:
    """Search a graph of A and B button presses for the solution."""
    if current == target:
        return path_len

    paths: list[int | None] = []

    next_a = (current[0] + a[0], current[1] + a[1])
    if next_a[0] <= target[0] and next_a[1] <= target[1]:
        paths.append(search_prize_graph(a, b, target, next_a, path_len + 3))

    next_b = (current[0] + b[0], current[1] + b[1])
    if next_b[0] <= target[0] and next_b[1] <= target[1]:
        paths.append(search_prize_graph(a, b, target, next_b, path_len + 1))

    _paths = [p for p in paths if p is not None]
    if _paths:
        return min(_paths)
    return None


def part_2(puzzle: str) -> int | str | float | bool:
    """Solution for AOC 2024, day 13, part 2."""
    sum = 0
    for config in itertools.batched(puzzle.splitlines(), 4):
        a = config[0][12:].split(", ", 1)
        a[1] = a[1].removeprefix("Y+")

        b = config[1][12:].split(", ", 1)
        b[1] = b[1].removeprefix("Y+")

        p = config[2][9:].split(", ", 1)
        p[1] = p[1].removeprefix("Y=")

        ax, ay, bx, by, px, py = (
            int(a[0]),
            int(a[1]),
            int(b[0]),
            int(b[1]),
            int(p[0]) + 10000000000000,
            int(p[1]) + 10000000000000,
        )

        # Had to look this up, systems of linear equations is the sort of maths I never
        # want to see again.
        # https://old.reddit.com/r/adventofcode/comments/1hd4wda/2024_day_13_solutions/m1ttnvc/
        y = (py * ax - px * ay) / (ax * by - ay * bx)
        x = (px - bx * y) / ax
        if int(x) == x and int(y) == y:
            sum += 3 * int(x) + int(y)

    return sum
