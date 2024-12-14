def part_1(puzzle: str) -> int | str | float | bool:
    """Solution for AOC 2024, day 6, part 1."""
    grid = TwoDGrid([list(line) for line in puzzle.splitlines()])
    grid.guard_walk()
    return len(grid.seen)


class TwoDGrid:  # noqa: D101
    def __init__(self, grid: list[list[str]]) -> None:
        self.grid = grid

        for x, row in enumerate(grid):
            for y, col in enumerate(row):
                if col == "^":
                    self.pos = (x, y)

        self.dir: tuple[int, int] = (-1, 0)
        self.seen = {self.pos}
        self.loop = {(self.pos, self.dir)}

    def guard_walk(self) -> bool:
        """
        Simulate the guard's walk through the map, returning `True` if we exit the map
        safely or `False` if we detect a loop.
        """
        while True:
            next = (self.pos[0] + self.dir[0], self.pos[1] + self.dir[1])
            if next[0] < 0 or next[0] >= len(self.grid):
                return True
            row = self.grid[next[0]]
            if next[1] < 0 or next[1] >= len(row):
                return True
            col = row[next[1]]

            if col == "#":
                self.turn_90()
            else:
                self.pos = next
                self.seen.add(next)

                if (self.pos, self.dir) in self.loop:
                    return False
                self.loop.add((self.pos, self.dir))

    def turn_90(self) -> None:
        """Rotate the guard's position 90 degrees (i.e. turn right)."""
        if self.dir == (-1, 0):
            self.dir = (0, 1)
        elif self.dir == (0, 1):
            self.dir = (1, 0)
        elif self.dir == (1, 0):
            self.dir = (0, -1)
        elif self.dir == (0, -1):
            self.dir = (-1, 0)
        else:
            raise ValueError(f"Unknown direction {self.dir}")


def part_2(puzzle: str) -> int | str | float | bool:
    """Solution for AOC 2024, day 6, part 2."""
    grid = TwoDGrid([list(line) for line in puzzle.splitlines()])
    x, y = len(grid.grid), len(grid.grid[0])
    loops = 0

    for row in range(x):
        for col in range(y):
            # Slow & dumb method: test putting an obstruction in each cell
            grid = TwoDGrid([list(line) for line in puzzle.splitlines()])

            cell = grid.grid[row][col]
            if cell in {"^", "#"}:
                continue

            grid.grid[row][col] = "#"
            if not grid.guard_walk():
                loops += 1

            grid.grid[row][col] = cell

    return loops
