"""AOC Day 14 started at 2022-12-14T15:30:01.842295+10:30"""  # noqa: D415


class Grid:  # noqa: D101
    def __init__(self) -> None:
        self.grid: list[list[str | None]] = []
        self._max_y = 0
        self._max_x = 0

    def set(self, x: int, y: int, value: str):  # noqa: ANN201, D102
        while len(self.grid) <= y:
            self.grid.append([])
        while len(self.grid[y]) <= x:
            self.grid[y].append(None)
        self.grid[y][x] = value
        self._max_y = max(self._max_y, y)
        self._max_x = max(self._max_x, x)

    def get(self, x: int, y: int) -> str | None:  # noqa: D102
        try:
            return self.grid[y][x]
        except IndexError:
            return None

    def set_line(self, x1: int, y1: int, x2: int, y2: int, value: str):  # noqa: ANN201, D102
        if x1 != x2 and y1 != y2:
            # Diagonal
            raise ValueError("diagonal lines not supported")
        if x1 == x2:
            # Vertical
            step = 1 if y1 < y2 + 1 else -1
            for y in range(y1, y2 + step, step):
                self.set(x1, y, value)
        elif y1 == y2:
            # Horizontal
            step = 1 if x1 < x2 + 1 else -1
            for x in range(x1, x2 + step, step):
                self.set(x, y1, value)

    def sand(self, x: int, y: int, value: str) -> tuple[int, int]:  # noqa: D102
        if y > self._max_y:
            raise ValueError(f"cannot place sand below {self._max_y=}")

        below = self.get(x, y + 1)
        if below is None:
            return self.sand(x, y + 1, value)

        below_left = self.get(x - 1, y + 1)
        if below_left is None and x - 1 >= 0:
            return self.sand(x - 1, y + 1, value)

        below_right = self.get(x + 1, y + 1)
        if below_right is None:
            return self.sand(x + 1, y + 1, value)

        self.set(x, y, value)
        return x, y

    def __str__(self) -> str:
        started = False
        lines = []
        for row in self.grid:
            line = "".join([str(v) if v is not None else "." for v in row])
            if line or started:
                started = True
                lines.append(line)
        return "\n".join(lines)

    def set_floor(self):  # noqa: ANN201, D102
        mx = self._max_x
        my = self._max_y + 2
        for x in range(mx * 2):
            self.set(x, my, "#")
        self._max_x = mx
        self._max_y = my


def part_1(puzzle: str):  # noqa: ANN201
    """Calculates the solution to day 14's first part."""
    grid = Grid()

    for line in puzzle.strip().splitlines():
        points = line.split(" -> ")

        for idx in range(len(points) - 1):
            grid.set_line(
                int(points[idx].split(",")[0]),
                int(points[idx].split(",")[1]),
                int(points[idx + 1].split(",")[0]),
                int(points[idx + 1].split(",")[1]),
                "#",
            )

    count = 0
    while True:
        try:
            grid.sand(500, 0, "o")
            count += 1
        except ValueError:
            return count


def part_2(puzzle: str):  # noqa: ANN201
    """Calculates the solution to day 14's second part."""
    grid = Grid()

    for line in puzzle.strip().splitlines():
        points = line.split(" -> ")

        for idx in range(len(points) - 1):
            grid.set_line(
                int(points[idx].split(",")[0]),
                int(points[idx].split(",")[1]),
                int(points[idx + 1].split(",")[0]),
                int(points[idx + 1].split(",")[1]),
                "#",
            )

    grid.set_floor()

    count = 0
    try:
        while grid.sand(500, 0, "o") != (500, 0):
            count += 1
    except ValueError:
        pass

    return count + 1  # +1 to account for last block of sand
