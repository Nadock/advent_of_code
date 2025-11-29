import builtins
from collections.abc import Generator


def part_1(puzzle: str) -> int | str | float | bool:
    """Solution for AOC 2024, day 20, part 1."""
    map = Map2D(puzzle)
    start, end = (0, 0), (0, 0)
    for p, v in map.iter():
        if v == "S":
            start = p
        if v == "E":
            end = p

    path = path_search(map, start, end)
    if not path:
        return "No path"
    cost = len(path[1:])  # don't count the start

    # print(start, end, cost, "\n", path)
    # print(map)

    cheats = find_cheat_points(map, path)
    print(f"{start=}, {end=}, {cost=}, {len(cheats)=}")

    min_reduction = 1 if len(puzzle.splitlines()) < 20 else 100
    reductions: dict[int, int] = {}

    for cheat in cheats:
        # start_cost = path.index(cheat[0]) + 1
        # end_cost = path.index(cheat[-1])
        # cheat_cost = len(cheat) - 2
        # print(
        #     f"{cheat=} goes from cost {start_cost} to {end_cost}, skipping {end_cost-start_cost-cheat_cost}"
        # )
        saving = path.index(cheat[-1]) - (path.index(cheat[0]) + 1) - (len(cheat) - 2)
        # print(f"{cheat=}, {saving=}")
        if saving >= min_reduction:
            reductions.setdefault(saving, 0)
            reductions[saving] += 1

    return sum(reductions.values())

    # # for p in path:
    # #     map.set(p, "O")
    # # print(map)
    # # map = Map2D(puzzle)

    # min_reduction = 1 if len(puzzle.splitlines()) < 20 else 100
    # reductions: dict[int, int] = {}

    # count = 0
    # for idx, cheat in enumerate(cheats):
    #     print(f"checking cheat {idx+1} of {len(cheats)}")
    #     # map = Map2D(puzzle)

    #     # old_points = []
    #     # for step in cheat[1:-1]:
    #     #     old_points.append(map.get(step))
    #     #     map.set(step, ".")

    #     path = path_search(map, start, end, cheat)
    #     if not path:
    #         return "no path"

    #     reduction = cost - len(path[1:])
    #     if reduction >= min_reduction:
    #         count += 1
    #         reductions.setdefault(reduction, 0)
    #         reductions[reduction] += 1

    return 0


def part_2(puzzle: str) -> int | str | float | bool:
    """Solution for AOC 2024, day 20, part 2."""
    map = Map2D(puzzle)
    start, end = (0, 0), (0, 0)
    for p, v in map.iter():
        if v == "S":
            start = p
        if v == "E":
            end = p

    path = map.cached_search(start, end)
    if not path:
        return "No path"
    cost = len(path[1:])  # don't count the start
    print(f"{start=}, {end=}, {cost=}, {len(path)=}")
    print(map)

    for point in path:
        cheat_ends = map.cheat_search(point, 20)
        print(f"{point=} has {len(cheat_ends)} cheat ends: {cheat_ends}")
        for p in cheat_ends:
            map.set(p, "X")
        print(map)
        break

    return "Part 2 TBD"


class Map2D:
    """A simple 2D grid style map."""

    def __init__(self, puzzle: str) -> None:
        self.grid: list[list[str]] = []

        lines = puzzle.splitlines()
        for column in range(len(lines[0])):
            self.grid.append([line[column] for line in lines if column < len(line)])

        self._solution_cache: dict[tuple[int, int], list[tuple[int, int]]] = {}

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

    def cached_search(
        self, s: tuple[int, int], e: tuple[int, int]
    ) -> list[tuple[int, int]]:
        moves = [([s], 0)]
        seen = set()
        solution = None
        while moves:
            path, score = moves.pop()
            current = path[-1]

            if current == e:
                solution = path
                break
            if current in self._solution_cache:
                solution = path[:-1] + self._solution_cache[current]
                break
            if current in seen:
                continue
            seen.add(current)

            next = [
                (current[0] + 1, current[1] + 0),
                (current[0] + -1, current[1] + 0),
                (current[0] + 0, current[1] + 1),
                (current[0] + 0, current[1] + -1),
            ]
            for move in next:
                if self.get(move) != "#":
                    moves.append(([*path, move], score + 1))

            moves.sort(key=lambda m: m[1], reverse=True)

        if not solution:
            raise ValueError(f"no path from {s} to {e}")

        for idx, p in enumerate(solution):
            self._solution_cache[p] = solution[idx:]
        return solution

    def cheat_search(
        self, p: tuple[int, int], max_depth=2
    ) -> builtins.set[tuple[int, int]]:
        moves = [(p, 0)]
        seen = set()
        ends = set()
        while moves:
            pos, dist = moves.pop()
            if dist > max_depth:
                continue
            if pos != p and self.get(pos) in {"S", "E", "."}:
                ends.add(pos)
                continue
            if pos in seen:
                continue
            seen.add(pos)

            moves = [
                *moves,
                ((pos[0] + 1, pos[1] + 0), dist + 1),
                ((pos[0] + -1, pos[1] + 0), dist + 1),
                ((pos[0] + 0, pos[1] + 1), dist + 1),
                ((pos[0] + 0, pos[1] + -1), dist + 1),
            ]
        return ends


def path_search(
    m: "Map2D",
    start: tuple[int, int],
    end: tuple[int, int],
) -> list[tuple[int, int]] | None:
    """Finds the minimum cost path from `start` to `end`."""
    moves = [([start], 0)]
    seen = set()
    while moves:
        path, score = moves.pop()
        current = path[-1]

        if current == end:
            return path
        if current in seen:
            continue
        seen.add(current)

        next = [
            (current[0] + 1, current[1] + 0),
            (current[0] + -1, current[1] + 0),
            (current[0] + 0, current[1] + 1),
            (current[0] + 0, current[1] + -1),
        ]
        for move in next:
            if m.get(move) != "#":
                moves.append(([*path, move], score + 1))

        moves.sort(key=lambda m: m[1], reverse=True)

    return None


def find_cheat_points(
    map: Map2D, path: list[tuple[int, int]]
) -> list[list[tuple[int, int]]]:
    cheats: list[list[tuple[int, int]]] = []

    for idx, p in enumerate(path):
        for dir in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            steps = [(p[0] + (dir[0] * i), p[1] + (dir[1] * i)) for i in range(1, 3)]

            cheat = [p]
            for step in steps:
                cheat.append(step)
                if map.get(step) != "#" or step in path:
                    break
            if cheat[-1] not in path:
                continue
            if path.index(cheat[-1]) < idx:
                continue

            cheats.append(cheat)

            # if any(map.get(s) == "#" for s in steps) and steps[-1] in path:
            #     cheats.add(tuple(steps))

    return cheats
