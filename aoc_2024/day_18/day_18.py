from collections.abc import Generator


def part_1(puzzle: str) -> int | str | float | bool:
    """Solution for AOC 2024, day 18, part 1."""
    positions = [
        (int(l.split(",", 1)[0]), int(l.split(",", 1)[1]))
        for l in puzzle.splitlines()
        if l
    ]

    size = 71 if len(positions) > 30 else 7
    map = Map2D("\n".join(["." * size for _ in range(size)]))

    start, end = (0, 0), (size - 1, size - 1)

    size = 1024 if size == 71 else 12
    for pos in positions[:size]:
        map.set(pos, "#")

    return optimal_path_cost(map, start, end) or "no solution"


def part_2(puzzle: str) -> int | str | float | bool:
    """Solution for AOC 2024, day 18, part 2."""
    positions = [
        (int(l.split(",", 1)[0]), int(l.split(",", 1)[1]))
        for l in puzzle.splitlines()
        if l
    ]

    size = 71 if len(positions) > 30 else 7
    map = Map2D("\n".join(["." * size for _ in range(size)]))

    start, end = (0, 0), (size - 1, size - 1)

    # Naive brute for search (slow)
    # for idx, pos in enumerate(positions):
    #     map.set(pos, "#")
    #     if optimal_path_cost(map, start, end) is None:
    #         return str(pos)

    # Much faster binary(-ish) search
    backtracking = False
    split = len(positions) // 2
    while split < len(positions):
        map = Map2D("\n".join(["." * size for _ in range(size)]))
        for pos in positions[:split]:
            map.set(pos, "#")

        dist = optimal_path_cost(map, start, end)
        if dist is not None:
            if backtracking:
                # We're back tracking but now we've worked our way back to one before
                # the final blocker.
                return str(positions[split])

            # We haven't blocked enough positions
            split = split + ((len(positions) - split) // 2)
        else:
            # We're past the first blocker, mark that we are now backtracking and move
            # back one.
            backtracking = True
            split = split - 1

    return "no solution"


class Map2D:
    """A simple 2D grid style map."""

    def __init__(self, puzzle: str) -> None:
        self.grid: list[list[str]] = []

        lines = puzzle.splitlines()
        for column in range(len(lines[0])):
            self.grid.append([line[column] for line in lines if column < len(line)])

    def __str__(self) -> str:
        lines = []
        for row in range(len(self.grid)):
            line = "".join([str(col[row]) for col in self.grid if row < len(col)])
            if line:
                lines.append(line)
        return "\n".join(lines)

    def get(self, p: tuple[int, int]) -> str | None:
        """
        Get the value at a point in the map, or `None` if the point is not in the map.
        """
        if p[0] < 0 or p[0] >= len(self.grid):
            return None
        col = self.grid[p[0]]
        if p[1] < 0 or p[1] >= len(col):
            return None
        return col[p[1]]

    def set(self, p: tuple[int, int], v: str) -> None:
        """Set the value of a point in the grid."""
        if p[0] < 0 or p[0] >= len(self.grid):
            raise IndexError(f"point {p} is not in the grid")
        col = self.grid[p[0]]
        if p[1] < 0 or p[1] >= len(col):
            raise IndexError(f"point {p} is not in the grid")
        self.grid[p[0]][p[1]] = v

    def iter(self) -> Generator[tuple[tuple[int, int], str]]:
        """Iterate through `(point, value)` pairs for every cell in the map."""
        for x in range(len(self.grid)):
            for y in range(len(self.grid[x])):
                yield (x, y), self.grid[x][y]


def optimal_path_cost(
    m: "Map2D", start: tuple[int, int], end: tuple[int, int]
) -> int | None:
    """Finds the minimum cost from `start` to `end`."""
    moves = [(start, 0)]
    seen = set()
    while moves:
        pos, score = moves.pop()
        if pos == end:
            return score
        if pos in seen:
            continue
        seen.add(pos)

        next = [
            (pos[0] + 1, pos[1] + 0),
            (pos[0] + -1, pos[1] + 0),
            (pos[0] + 0, pos[1] + 1),
            (pos[0] + 0, pos[1] + -1),
        ]
        for move in next:
            if m.get(move) == ".":
                moves.append((move, score + 1))  # noqa: PERF401

        moves.sort(key=lambda m: m[1], reverse=True)

    return None
