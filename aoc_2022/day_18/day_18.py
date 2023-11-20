"""AOC Day 18 started at 2022-12-18T15:30:07.767578+10:30"""
import functools


def part_1(puzzle: str):
    """Calculates the solution to day 18's first part."""
    scan_grid: dict[tuple[int, int, int], bool] = {}
    for line in puzzle.strip().splitlines():
        x = int(line.split(",")[0])
        y = int(line.split(",")[1])
        z = int(line.split(",")[2])
        scan_grid[(x, y, z)] = True

    return count_exposed_faces(scan_grid)


def part_2(puzzle: str):
    """Calculates the solution to day 18's second part."""
    scan_grid: dict[tuple[int, int, int], bool] = {}
    grid_min, grid_max = (0, 0, 0), (0, 0, 0)
    for line in puzzle.strip().splitlines():
        x = int(line.split(",")[0])
        y = int(line.split(",")[1])
        z = int(line.split(",")[2])

        grid_min = (min(grid_min[0], x), min(grid_min[1], y), min(grid_min[2], z))
        grid_max = (max(grid_max[0], x), max(grid_max[1], y), max(grid_max[2], z))

        scan_grid[(x, y, z)] = True

    return count_external_faces(scan_grid, grid_min, grid_max)


def count_exposed_faces(grid: dict[tuple[int, int, int], bool]) -> int:
    exposed_faces = 0

    for (x, y, z), is_filled in grid.items():
        if is_filled:
            exposed_faces += len(
                [
                    f
                    for f in [
                        grid.get((x + 1, y, z), False),
                        grid.get((x - 1, y, z), False),
                        grid.get((x, y + 1, z), False),
                        grid.get((x, y - 1, z), False),
                        grid.get((x, y, z + 1), False),
                        grid.get((x, y, z - 1), False),
                    ]
                    if not f
                ],
            )

    return exposed_faces


def count_external_faces(grid: dict[tuple[int, int, int], bool], g_min, g_max) -> int:
    @functools.lru_cache
    def dfs_edge_search(x, y, z):
        stack = [(x, y, z)]
        seen = set()
        while stack:
            (x, y, z) = stack.pop()
            if (x, y, z) in grid:
                continue
            if (x, y, z) in seen:
                continue
            seen.add((x, y, z))
            if (
                x <= g_min[0]
                or y <= g_min[1]
                or z <= g_min[2]
                or x >= g_max[0]
                or y >= g_max[1]
                or z >= g_max[2]
            ):
                return True
            stack.append((x + 1, y, z))
            stack.append((x - 1, y, z))
            stack.append((x, y + 1, z))
            stack.append((x, y - 1, z))
            stack.append((x, y, z + 1))
            stack.append((x, y, z - 1))
        return False

    exposed = 0
    for x, y, z in grid.keys():
        faces = [
            (x + 1, y, z),
            (x - 1, y, z),
            (x, y + 1, z),
            (x, y - 1, z),
            (x, y, z + 1),
            (x, y, z - 1),
        ]
        for fx, fy, fz in faces:
            if dfs_edge_search(fx, fy, fz):
                exposed += 1

    return exposed
