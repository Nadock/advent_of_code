from collections.abc import Generator


def part_1(puzzle: str) -> int | str | float | bool:
    """Solution for AOC 2023, day 6, part 1."""
    times = [int(t) for t in puzzle.splitlines()[0].split("Time: ", 1)[1].split()]
    dists = [int(d) for d in puzzle.splitlines()[1].split("Distance: ", 1)[1].split()]

    multi = 1

    for time, dist in zip(times, dists, strict=True):
        count = 0
        for v, t in iter_v_t(time):
            d = v * t
            if d > dist:
                count += 1
        multi *= count

    return multi


def iter_v_t(time: int) -> Generator[tuple[int, int], None, None]:  # noqa: D103
    for i in range(time):
        v = time - i
        t = time - v
        yield v, t


def part_2(puzzle: str) -> int | str | float | bool:
    """Solution for AOC 2023, day 6, part 2."""
    time = int("".join(puzzle.splitlines()[0].split("Time: ", 1)[1].split()))
    dist = int("".join(puzzle.splitlines()[1].split("Distance: ", 1)[1].split()))

    count = 0
    for v, t in iter_v_t(time):
        d = v * t
        if d > dist:
            count += 1

    return count
