"""AOC Day 15 started at 2022-12-15T15:30:03.100645+10:30"""  # noqa: D415


class Grid:  # noqa: D101
    def __init__(self) -> None:
        self.grid = {}
        self.min = (0, 0)
        self.max = (0, 0)

    def set(self, x, y, value):  # noqa: ANN001, ANN201, D102
        self.grid.setdefault(x, {})
        self.grid[x][y] = value
        self.min = (min(self.min[0], x), min(self.min[1], y))
        self.max = (max(self.max[0], x), max(self.max[1], y))

    def get(self, x, y):  # noqa: ANN001, ANN201, D102
        self.grid.setdefault(x, {})
        return self.grid[x].get(y)

    def rows(self) -> list[list]:  # noqa: D102
        rows = []
        for y in range(self.min[1], self.max[1] + 1):
            rows.append(self.row(y))  # noqa: PERF401
        return rows

    def row(self, y: int) -> list:  # noqa: D102
        row = []
        for x in range(self.min[0], self.max[0] + 1):
            row.append(self.get(x, y))  # noqa: PERF401
        return row


def part_1(puzzle: str):  # noqa: ANN201
    """Calculates the solution to day 15's first part."""
    grid = Grid()

    for line in puzzle.strip().splitlines():
        # 0      1  2    3     4       5      6  7  8     9
        # Sensor at x=2, y=18: closest beacon is at x=-2, y=15
        splits = line.split(" ")

        s_x = int(splits[2].replace("x=", "").replace(",", ""))
        s_y = int(splits[3].replace("y=", "").replace(":", ""))
        sensor = (s_x, s_y)

        b_x = int(splits[8].replace("x=", "").replace(",", ""))
        b_y = int(splits[9].replace("y=", "").replace(":", ""))
        beacon = (b_x, b_y)

        dist = manhattan_distance(sensor, beacon)

        grid.set(s_x, s_y, "S")
        grid.set(b_x, b_y, "B")

        for x in range(sensor[0] - dist, sensor[0] + dist + 1):
            for y in range(2000000, 2000001):
                if manhattan_distance((x, y), sensor) <= dist:  # noqa: SIM102
                    if grid.get(x, y) is None:
                        grid.set(x, y, "#")

    return len([v for v in grid.row(2000000) if v == "#"])


def manhattan_distance(p1: tuple[int, int], p2: tuple[int, int]) -> int:  # noqa: D103
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


def part_2(puzzle: str):  # noqa: ANN201
    """Calculates the solution to day 15's second part."""
    grid = Grid()

    sensors = []
    blocked = {}

    for line in puzzle.strip().splitlines():
        # 0      1  2    3     4       5      6  7  8     9
        # Sensor at x=2, y=18: closest beacon is at x=-2, y=15
        splits = line.split(" ")

        s_x = int(splits[2].replace("x=", "").replace(",", ""))
        s_y = int(splits[3].replace("y=", "").replace(":", ""))
        sensor = (s_x, s_y)

        b_x = int(splits[8].replace("x=", "").replace(",", ""))
        b_y = int(splits[9].replace("y=", "").replace(":", ""))
        beacon = (b_x, b_y)

        dist = manhattan_distance(sensor, beacon)
        sensors.append((sensor, dist))

        grid.set(s_x, s_y, "S")
        grid.set(b_x, b_y, "B")

        for offset in range(dist + 1):
            blocked.setdefault(sensor[1] + offset, [])
            blocked.setdefault(sensor[1] - offset, [])

            x0 = max(0, sensor[0] - (dist - offset))
            x1 = min(4_000_000, sensor[0] + (dist - offset)) + 1
            r = (min(x0, x1), max(x0, x1))

            blocked[sensor[1] + offset].append(r)
            blocked[sensor[1] - offset].append(r)

    for y in range(4_000_001):  # noqa: RET503
        blocked[y] = sorted(blocked[y], key=lambda b: b[0])

        if blocked[y][0][0] != 0:
            raise ValueError(f"blockers on line {y} start at {blocked[y][0][0]} not 0")

        end = blocked[y][0][1]
        for blocker in blocked[y]:
            if end > 4_000_000:  # noqa: PLR2004
                break
            if end < blocker[0]:
                return (end * 4_000_000) + y

            end = max(end, blocker[1])
