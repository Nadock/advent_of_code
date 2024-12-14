from collections.abc import Generator


def part_1(puzzle: str) -> int | str | float | bool:
    """Solution for AOC 2024, day 10, part 1."""
    m = Map2D(puzzle)
    score = 0
    for p, v in m.iter():
        if v == 0:
            trails = trail_search(m, p)
            # Count unique trail ends
            score += len({t[-1] for t in trails})

    return score


def trail_search(
    m: "Map2D", start: tuple[int, int], path: list[tuple[int, int]] | None = None
) -> list[list[tuple[int, int]]]:
    """BFS algorithm according to the trail rules in the puzzle."""
    if not path:
        path = []

    s_value = m.at(start)
    if s_value is None or s_value == 9:
        return [path]

    up = (start[0], start[1] + 1)
    down = (start[0], start[1] - 1)
    right = (start[0] + 1, start[1])
    left = (start[0] - 1, start[1])

    new_paths: list[list[tuple[int, int]]] = []
    for d in [up, down, right, left]:
        if m.at(d) == s_value + 1:
            new_path = trail_search(m, d, [*path, d])
            if new_path:
                new_paths += new_path

    return new_paths


def part_2(puzzle: str) -> int | str | float | bool:
    """Solution for AOC 2024, day 10, part 2."""
    m = Map2D(puzzle)
    score = 0
    for p, v in m.iter():
        if v == 0:
            trails = trail_search(m, p)
            # Count unique paths
            score += len(trails)

    return score


class Map2D:
    """A simple 2D grid style map."""

    def __init__(self, puzzle: str) -> None:
        self.grid = []

        lines = puzzle.splitlines()
        for column in range(len(lines[0])):
            col = []
            for line in lines:
                if line[column] != ".":
                    col.append(int(line[column]))
                else:
                    col.append(-1)
            self.grid.append(col)

    def __str__(self) -> str:
        s = ""
        for row in range(len(self.grid)):
            s += "".join([str(col[row]) for col in self.grid])
            s += "\n"
        return s

    def at(self, p: tuple[int, int]) -> int | None:
        """
        Get the value at a point in the map, or `None` if the point is not in the map.
        """
        if p[0] < 0 or p[0] >= len(self.grid):
            return None
        col = self.grid[p[0]]
        if p[1] < 0 or p[1] >= len(col):
            return None
        return col[p[1]]

    def iter(self) -> Generator[tuple[tuple[int, int], int]]:
        """Iterate through `(point, value)` pairs for every cell in the map."""
        for x in range(len(self.grid)):
            for y in range(len(self.grid[x])):
                yield (x, y), self.grid[x][y]
