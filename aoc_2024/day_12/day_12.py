from collections.abc import Generator


def part_1(puzzle: str) -> int | str | float | bool:
    """Solution for AOC 2024, day 12, part 1."""
    m = Map2D(puzzle)

    sum = 0
    for r in find_regions(m):
        area = region_area(r)
        perimeter = region_perimeter(m, r)
        cost = area * perimeter
        sum += cost

    return sum


def find_regions(m: "Map2D") -> list[set[tuple[int, int]]]:
    """Find sets of points that form contiguous regions in the map."""
    regions: list[set[tuple[int, int]]] = []
    seen: set[tuple[int, int]] = set()

    for p, _ in m.iter():
        if p not in seen:
            region = find_region(m, p)
            seen = seen.union(region)
            regions.append(region)

    return regions


def find_region(
    m: "Map2D", start: tuple[int, int], region: set[tuple[int, int]] | None = None
) -> set[tuple[int, int]]:
    """
    Find all the points for a single region starting at a given `start` point.

    The `region` parameter is used for recursive calls.
    """
    if not region:
        region = set()

    # Out of map bounds
    if not m.at(start):
        return region
    # Out of region bounds
    if region and m.at(start) != m.at(next(iter(region))):
        return region
    # Already in region
    if start in region:
        return region

    region.add(start)

    up = (start[0], start[1] + 1)
    down = (start[0], start[1] - 1)
    right = (start[0] + 1, start[1])
    left = (start[0] - 1, start[1])

    for d in [up, down, left, right]:
        region = region.union(find_region(m, d, region))

    return region


def region_area(r: set[tuple[int, int]]) -> int:
    """Count the total area for a region."""
    return len(r)


def region_perimeter(m: "Map2D", r: set[tuple[int, int]]) -> int:
    """Count the perimeter for a region."""
    perimeter = 0

    for p in r:
        up = (p[0], p[1] + 1)
        down = (p[0], p[1] - 1)
        right = (p[0] + 1, p[1])
        left = (p[0] - 1, p[1])

        for d in [up, down, left, right]:
            if m.at(d) is None or m.at(d) != m.at(p):
                perimeter += 1

    return perimeter


def region_sides(m: "Map2D", r: set[tuple[int, int]]) -> int:
    """Count the sides of a region."""
    sides = 0

    # Top sides
    sides += count_direction_sides(m, r, (0, -1))
    # Bottom sides
    sides += count_direction_sides(m, r, (0, 1))
    # Left sides
    sides += count_direction_sides(m, r, (-1, 0))
    # Right sides
    sides += count_direction_sides(m, r, (1, 0))

    return sides


def count_direction_sides(  # noqa: PLR0912
    m: "Map2D", r: set[tuple[int, int]], direction: tuple[int, int]
) -> int:
    """
    Count the sides of a region in a particular direction.

    Where direction is `(0, -1)` for up, `(0, 1)` for down, `(-1 ,0)` for left, or
    `(1, 0)` for right.
    """
    # Find all the points that form the side in the given direction
    side_points = []
    for p in r:
        d = (p[0] + direction[0], p[1] + direction[1])
        if m.at(p) != m.at(d):
            side_points.append(d)

    # Sort by common y if up or down, or by common x if left or right
    if direction[0] == 0:
        side_points.sort(key=lambda p: (p[1], p[0]))
    else:
        side_points.sort(key=lambda p: (p[0], p[1]))

    sides = []

    side: list[tuple[int, int]] = []
    for p in side_points:
        if not side:
            side.append(p)
            continue
        # Up/Down sides
        if direction[0] == 0:
            if side[-1][0] + 1 == p[0] and side[-1][1] == p[1]:
                side.append(p)
            else:
                if len(side) > 1:
                    sides.append(side)
                side = [p]
        # Left/Right sides
        else:  # noqa: PLR5501
            if side[-1][0] == p[0] and side[-1][1] + 1 == p[1]:
                side.append(p)
            else:
                if len(side) > 1:
                    sides.append(side)
                side = [p]

    if len(side) > 1:
        sides.append(side)

    # Remove all side points that have been grouped into longer sides
    for side in sides:
        for p in side:
            side_points.remove(p)

    return len(sides + side_points)


def part_2(puzzle: str) -> int | str | float | bool:
    """Solution for AOC 2024, day 12, part 2."""
    m = Map2D(puzzle)

    sum = 0
    for r in find_regions(m):
        area = region_area(r)
        sides = region_sides(m, r)
        cost = area * sides
        sum += cost

    return sum


class Map2D:
    """A simple 2D grid style map."""

    def __init__(self, puzzle: str) -> None:
        self.grid: list[list[str]] = []

        lines = puzzle.splitlines()
        for column in range(len(lines[0])):
            self.grid.append([line[column] for line in lines])

    def __str__(self) -> str:
        s = ""
        for row in range(len(self.grid)):
            s += "".join([str(col[row]) for col in self.grid])
            s += "\n"
        return s

    def at(self, p: tuple[int, int]) -> str | None:
        """
        Get the value at a point in the map, or `None` if the point is not in the map.
        """
        if p[0] < 0 or p[0] >= len(self.grid):
            return None
        col = self.grid[p[0]]
        if p[1] < 0 or p[1] >= len(col):
            return None
        return col[p[1]]

    def iter(self) -> Generator[tuple[tuple[int, int], str]]:
        """Iterate through `(point, value)` pairs for every cell in the map."""
        for x in range(len(self.grid)):
            for y in range(len(self.grid[x])):
                yield (x, y), self.grid[x][y]
