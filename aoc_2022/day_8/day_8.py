"""AOC Day 8 started at 2022-12-08T20:28:51.652941+10:30"""  # noqa: D415


def part_1(puzzle: str):  # noqa: ANN201
    """Calculates the solution to day 8's first part."""
    grid = []
    for line in puzzle.splitlines():
        grid.append([int(c) for c in line])  # noqa: PERF401

    visible_trees = 0

    for row, r in enumerate(grid):
        for col, tree in enumerate(r):
            visible = []
            for i in range(row):
                if grid[i][col] >= tree:
                    visible.append(True)
                    break
            for i in range(row + 1, len(grid)):
                if grid[i][col] >= tree:
                    visible.append(True)
                    break
            for i in range(col):
                if r[i] >= tree:
                    visible.append(True)
                    break
            for i in range(col + 1, len(r)):
                if r[i] >= tree:
                    visible.append(True)
                    break

            if len(visible) != 4:
                visible_trees += 1

    return visible_trees


def part_2(puzzle: str):  # noqa: ANN201
    """Calculates the solution to day 8's second part."""
    grid = []
    for line in puzzle.splitlines():
        grid.append([int(c) for c in line])  # noqa: PERF401

    s_max = 0

    for row, r in enumerate(grid):
        for col, tree in enumerate(r):
            s_sore = (
                len(up(grid, row, col, tree))
                * len(down(grid, row, col, tree))
                * len(left(grid, row, col, tree))
                * len(right(grid, row, col, tree))
            )

            s_max = max(s_sore, s_max)

    return s_max


def up(grid: list[list[int]], row: int, col: int, limit: int) -> list[int]:  # noqa: D103
    l = []
    for r in range(row - 1, -1, -1):
        l.append(grid[r][col])
        if grid[r][col] >= limit:
            break
    return l


def down(grid: list[list[int]], row: int, col: int, limit: int) -> list[int]:  # noqa: D103
    l = []
    for r in range(row + 1, len(grid)):
        l.append(grid[r][col])
        if grid[r][col] >= limit:
            break
    return l


def left(grid: list[list[int]], row: int, col: int, limit: int) -> list[int]:  # noqa: D103
    l = []
    for c in range(col - 1, -1, -1):
        l.append(grid[row][c])
        if grid[row][c] >= limit:
            break
    return l


def right(grid: list[list[int]], row: int, col: int, limit: int) -> list[int]:  # noqa: D103
    l = []
    for c in range(col + 1, len(grid[row])):
        l.append(grid[row][c])
        if grid[row][c] >= limit:
            break
    return l
