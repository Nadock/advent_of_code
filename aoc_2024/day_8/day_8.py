import fractions
import itertools


def part_1(puzzle: str) -> int | str | float | bool:
    """Solution for AOC 2024, day 8, part 1."""
    grid = [list(row) for row in puzzle.splitlines()]

    frequencies: dict[str, list[tuple[int, int]]] = {}

    for x, col in enumerate(grid):
        for y, cell in enumerate(col):
            if cell != ".":
                frequencies.setdefault(cell, [])
                frequencies[cell].append((x, y))

    for coords in frequencies.values():
        for a, b in itertools.combinations(coords, r=2):
            dx = a[0] - b[0]
            dy = a[1] - b[1]

            anti_a = (a[0] + dx, a[1] + dy)
            anti_b = (b[0] - dx, b[1] - dy)

            if (
                anti_a[0] >= 0
                and anti_a[0] < len(grid)
                and anti_a[1] >= 0
                and anti_a[1] < len(grid[anti_a[0]])
            ):
                grid[anti_a[0]][anti_a[1]] = "#"
            if (
                anti_b[0] >= 0
                and anti_b[0] < len(grid)
                and anti_b[1] >= 0
                and anti_b[1] < len(grid[anti_b[0]])
            ):
                grid[anti_b[0]][anti_b[1]] = "#"

    count = 0
    for row in grid:
        for cell in row:
            if cell == "#":
                count += 1

    return count


def part_2(puzzle: str) -> int | str | float | bool:
    """Solution for AOC 2024, day 8, part 2."""
    grid = [list(row) for row in puzzle.splitlines()]
    frequencies: dict[str, list[tuple[int, int]]] = {}

    for x, col in enumerate(grid):
        for y, cell in enumerate(col):
            if cell != ".":
                frequencies.setdefault(cell, [])
                frequencies[cell].append((x, y))

    for coords in frequencies.values():
        for a, b in itertools.combinations(coords, r=2):
            slope = fractions.Fraction((a[1] - b[1]), (a[0] - b[0]))

            for x in range(len(grid)):
                for y in range(len(grid[x])):
                    if a[0] - x == 0:
                        continue
                    new_slope = fractions.Fraction(a[1] - y, a[0] - x)
                    if slope == new_slope and grid[x][int(y)] == ".":
                        grid[x][int(y)] = "#"

    count = 0
    for row in grid:
        for cell in row:
            if cell != ".":
                count += 1

    return count
