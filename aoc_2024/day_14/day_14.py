import math


def part_1(puzzle: str) -> int | str | float | bool:
    """Solution for AOC 2024, day 14, part 1."""
    robots = []
    max_x, max_y = 0, 0
    for line in puzzle.splitlines():
        p = (
            int(line.split(" ", 1)[0][2:].split(",")[0]),
            int(line.split(" ", 1)[0][2:].split(",")[1]),
        )
        max_x = max(p[0], max_x)
        max_y = max(p[1], max_y)
        v = (
            int(line.split(" ", 1)[1][2:].split(",")[0]),
            int(line.split(" ", 1)[1][2:].split(",")[1]),
        )
        robots.append((p, v))

    robots = [simulate_robot(r, (max_x, max_y)) for r in robots]

    mid_x, mid_y = max_x / 2, max_y / 2
    quads = [0, 0, 0, 0]
    for robot in robots:
        if robot[0][0] < mid_x and robot[0][1] < mid_y:
            quads[0] += 1
        elif robot[0][0] > mid_x and robot[0][1] < mid_y:
            quads[1] += 1
        elif robot[0][0] < mid_x and robot[0][1] > mid_y:
            quads[2] += 1
        elif robot[0][0] > mid_x and robot[0][1] > mid_y:
            quads[3] += 1

    return math.prod(quads)


def simulate_robot(
    robot: tuple[tuple[int, int], tuple[int, int]],
    max: tuple[int, int],
    iters: int = 100,
) -> tuple[tuple[int, int], tuple[int, int]]:
    """Simulate a robot according to the puzzle rules `iters` times."""
    for _ in range(iters):
        px = (robot[0][0] + robot[1][0]) % (max[0] + 1)
        py = (robot[0][1] + robot[1][1]) % (max[1] + 1)
        robot = ((px, py), robot[1])
    return robot


def part_2(puzzle: str) -> int | str | float | bool:
    """Solution for AOC 2024, day 14, part 2."""
    robots = []
    max_x, max_y = 0, 0
    for line in puzzle.splitlines():
        p = (
            int(line.split(" ", 1)[0][2:].split(",")[0]),
            int(line.split(" ", 1)[0][2:].split(",")[1]),
        )
        max_x = max(p[0], max_x)
        max_y = max(p[1], max_y)
        v = (
            int(line.split(" ", 1)[1][2:].split(",")[0]),
            int(line.split(" ", 1)[1][2:].split(",")[1]),
        )
        robots.append((p, v))

    # Check if all robots in unique positions — this only happens when the christmas
    # tree easter egg appears. Not that this is guaranteed in any way, it just works out
    # that way.
    for i in range(1_000_000):
        robots = [simulate_robot(r, (max_x, max_y), 1) for r in robots]
        is_unique = True
        seen = set()
        for r in robots:
            if r[0] not in seen:
                seen.add(r[0])
            else:
                is_unique = False
                break

        if is_unique:
            return i + 1
    return "try a larger number"
