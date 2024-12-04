def part_1(puzzle: str) -> int | str | float | bool:
    """Solution for AOC 2024, day 4, part 1."""
    grid = [list(line) for line in puzzle.splitlines()]

    sum = 0
    for row, r in enumerate(grid):
        for col, _ in enumerate(r):
            sum += find_xmas_linear(grid, row=row, col=col)

    return sum


def find_xmas_linear(
    grid: list[list[str]],
    *,
    row: int,
    col: int,
    current: str = "",
    offset: tuple[int, int] | None = None,
) -> int:
    """
    Count the number of "XMAS" strings in a linear direction (up, down, left, right, or
    diagonally), either forwards or backwards, from a starting position in the grid.

    `current` and `offset` are recursion call parameters only.
    """
    if current == "XMAS":
        return 1

    if (
        len(current) == 4
        or row >= len(grid)
        or row < 0
        or col >= len(grid[row])
        or col < 0
    ):
        return 0

    current += grid[row][col]

    if offset:
        return find_xmas_linear(
            grid,
            row=row + offset[0],
            col=col + offset[1],
            current=current,
            offset=offset,
        )

    sum = 0
    for r in range(-1, 2):
        for c in range(-1, 2):
            sum += find_xmas_linear(
                grid, row=row + r, col=col + c, current=current, offset=(r, c)
            )

    return sum


def part_2(puzzle: str) -> int | str | float | bool:
    """Solution for AOC 2024, day 4, part 2."""
    grid = [list(line) for line in puzzle.splitlines()]
    sum = 0
    for row, r in enumerate(grid):
        for col, char in enumerate(r):
            if char == "A":
                sum += find_mas_cross(grid, row=row, col=col)

    return sum


def find_mas_cross(grid: list[list[str]], row: int, col: int) -> int:
    """Find a "MAS" cross in the grid from a good starting cell."""
    if row + 1 >= len(grid) or row - 1 < 0 or col + 1 >= len(grid[row]) or col - 1 < 0:
        return 0

    left = grid[row - 1][col - 1] + grid[row][col] + grid[row + 1][col + 1]
    right = grid[row - 1][col + 1] + grid[row][col] + grid[row + 1][col - 1]

    if right in ("MAS", "SAM") and left in ("MAS", "SAM"):
        return 1

    return 0
