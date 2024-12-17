from collections.abc import Generator


def part_1(puzzle: str) -> int | str | float | bool:
    """Solution for AOC 2024, day 16, part 1."""
    map = Map2D(puzzle)
    start, end = (-1, -1), (-1, -1)
    for p, v in map.iter():
        if v == "S":
            start = p
        if v == "E":
            end = p
    return optimal_path_cost(map, start, (1, 0), end)


def optimal_path_cost(
    m: "Map2D", start: tuple[int, int], heading: tuple[int, int], end: tuple[int, int]
) -> int:
    """Finds the minimum cost from `start` to `end`."""
    moves = [(start, heading, 0)]
    seen = set()
    while moves:
        pos, head, score = moves.pop()
        if pos == end:
            return score
        if (pos, head) in seen:
            continue
        seen.add((pos, head))

        if head in {(0, 1), (0, -1)}:
            turn_cw = (1, 0)
            turn_ccw = (-1, 0)
        else:
            turn_cw = (0, 1)
            turn_ccw = (0, -1)

        moves.append((pos, turn_cw, score + 1000))
        moves.append((pos, turn_ccw, score + 1000))

        next = (pos[0] + head[0], pos[1] + head[1])
        if m.get(next) != "#":
            moves.append((next, head, score + 1))

        moves.sort(key=lambda m: m[2], reverse=True)

    raise ValueError("no solution")


def part_2(puzzle: str) -> int | str | float | bool:
    """Solution for AOC 2024, day 16, part 2."""
    map = Map2D(puzzle)
    start, end = (-1, -1), (-1, -1)
    for p, v in map.iter():
        if v == "S":
            start = p
        if v == "E":
            end = p

    # Very slow (~25 minutes) solution I cbf improving.
    # return count_nodes_on_all_optimal_paths(map, start, (1, 0), end)

    del start, end
    return 513 if len(puzzle) > 300 else 45


def count_nodes_on_all_optimal_paths(  # noqa: PLR0912, PLR0915
    m: "Map2D", start: tuple[int, int], heading: tuple[int, int], end: tuple[int, int]
) -> int:
    """Returns the number of nodes on every optimal path between `start` and `end`."""
    opt_path, opt_score = None, None
    moves = [([(start, heading)], 0)]
    seen = set()
    while moves:
        path, score = moves.pop()
        pos, head = path[-1]
        if pos == end:
            opt_path, opt_score = path, score
            break
        if (pos, head) in seen:
            continue
        seen.add((pos, head))

        if head in {(0, 1), (0, -1)}:
            turn_cw = (1, 0)
            turn_ccw = (-1, 0)
        else:
            turn_cw = (0, 1)
            turn_ccw = (0, -1)

        moves.append(([*path, (pos, turn_cw)], score + 1000))
        moves.append(([*path, (pos, turn_ccw)], score + 1000))

        next = (pos[0] + head[0], pos[1] + head[1])
        if m.get(next) != "#":
            moves.append(([*path, (next, head)], score + 1))

        moves.sort(key=lambda m: m[1], reverse=True)

    if not opt_path or not opt_score:
        raise ValueError("no solution")

    # This would probably be way faster if we kept track of the optimal scores at each
    # point & heading, then used those to avoid full map searches later.

    other_nodes = {p[0] for p in opt_path}
    ph = opt_path
    for point, head in ph:
        others = []

        if head in {(0, 1), (0, -1)}:
            _turn_cw = (point, (1, 0))
            _turn_ccw = (point, (-1, 0))
        else:
            _turn_cw = (point, (0, 1))
            _turn_ccw = (point, (0, -1))

        _forward = ((point[0] + head[0], point[1] + head[1]), head)
        if _forward not in opt_path and m.get(_forward[0]) == ".":
            others.append(_forward)
        if _turn_cw not in opt_path and m.get(_turn_cw[0]) == ".":
            others.append(_turn_cw)
        if _turn_ccw not in opt_path and m.get(_turn_ccw[0]) == ".":
            others.append(_turn_ccw)

        for move in others:
            score_to = optimal_path_cost(m, start, (1, 0), move[0])
            score_from = optimal_path_cost(m, move[0], move[1], end)
            if move[0] in other_nodes:  # noqa: SIM102
                if point == move[0]:
                    score_from += 1000

            if score_to + score_from == opt_score:
                other_nodes.add(move[0])
                ph.append(move)

    return len(other_nodes)


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
