from collections.abc import Generator
from copy import deepcopy


def part_1(puzzle: str) -> int | str | float | bool:
    """Solution for AOC 2024, day 15, part 1."""
    map = Map2D(puzzle.split("\n\n", 1)[0])
    moves = list(puzzle.split("\n\n", 1)[1].replace("\n", "").strip())

    robot = (-1, -1)
    for p, v in map.iter():
        if v == "@":
            robot = p
            break

    for move in moves:
        next_pt = map.direction_to_point(robot, move)
        map.push(next_pt, move)
        if map.get(next_pt) == ".":
            map.set(robot, ".")
            robot = next_pt
            map.set(robot, "@")

    sum = 0
    for p, v in map.iter():
        if v == "O":
            sum += p[0] + p[1] * 100

    return sum


def part_2(puzzle: str) -> int | str | float | bool:
    """Solution for AOC 2024, day 15, part 2."""
    # Make the map bigger
    raw_map = (
        puzzle.split("\n\n", 1)[0]
        .replace("#", "##")
        .replace("O", "[]")
        .replace(".", "..")
        .replace("@", "@.")
    )

    map = Map2D(raw_map)
    moves = list(puzzle.split("\n\n", 1)[1].replace("\n", "").strip())

    robot = (-1, -1)
    for p, v in map.iter():
        if v == "@":
            robot = p
            break

    for move in moves:
        next_pt = map.direction_to_point(robot, move)

        # If the push is invalid, reset the map
        before = deepcopy(map.grid)
        if not map.push2(next_pt, move):
            map.grid = before

        if map.get(next_pt) == ".":
            map.set(robot, ".")
            robot = next_pt
            map.set(robot, "@")

    sum = 0
    for p, v in map.iter():
        if v == "[":
            sum += p[0] + p[1] * 100

    return sum


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

    def direction_to_point(self, p: tuple[int, int], direction: str) -> tuple[int, int]:
        """Given a point and a direction, return the next point in that direction."""
        match direction:
            case "^":
                return (p[0], p[1] - 1)
            case "v":
                return (p[0], p[1] + 1)
            case "<":
                return (p[0] - 1, p[1])
            case ">":
                return (p[0] + 1, p[1])
            case _:
                raise ValueError(f"unknown {direction=}")

    def push(self, p: tuple[int, int], direction: str) -> None:
        """Push a barrel according to the part 1 rules."""
        if self.get(p) != "O":
            # Can't push something that isn't a barrel
            return

        d = self.direction_to_point(p, direction)

        if self.get(d) == "#":
            # Can't move walls
            return

        if self.get(d) == "O":
            # Try and push the barrel in the specified direction
            self.push(d, direction)

        if self.get(d) == ".":
            # Move barrel into free space
            self.set(d, "O")
            self.set(p, ".")

    def push2(self, p: tuple[int, int], direction: str) -> bool:  # noqa: PLR0912, PLR0915
        """
        Push a barrel according to the part 2 rules.

        Returns false if a push is invalid, the map state must be reset.
        """
        if self.get(p) not in {"[", "]"}:
            # Can't push something that isn't a barrel
            return True

        if self.get(p) == "[":
            barrel_l = p
            barrel_r = (p[0] + 1, p[1])
        else:
            barrel_l = (p[0] - 1, p[1])
            barrel_r = p

        dirty = False
        match direction:
            case "^":
                up_l, up_r = (
                    (barrel_l[0], barrel_l[1] - 1),
                    (barrel_r[0], barrel_r[1] - 1),
                )
                if not self.push2(up_l, "^") or not self.push2(up_r, "^"):
                    dirty = True

                if self.get(up_l) == "." and self.get(up_r) == ".":
                    self.set(up_l, "[")
                    self.set(up_r, "]")
                    self.set(barrel_l, ".")
                    self.set(barrel_r, ".")
                else:
                    dirty = True

            case "v":
                down_l, down_r = (
                    (barrel_l[0], barrel_l[1] + 1),
                    (barrel_r[0], barrel_r[1] + 1),
                )
                if not self.push2(down_l, "v") or not self.push2(down_r, "v"):
                    dirty = True

                if self.get(down_l) == "." and self.get(down_r) == ".":
                    self.set(down_l, "[")
                    self.set(down_r, "]")
                    self.set(barrel_l, ".")
                    self.set(barrel_r, ".")
                else:
                    dirty = True

            case "<":
                left = (barrel_l[0] - 1, barrel_l[1])
                if not self.push2(left, "<"):
                    dirty = True

                if self.get(left) == ".":
                    self.set(left, "[")
                    self.set(barrel_l, "]")
                    self.set(barrel_r, ".")
                else:
                    dirty = True

            case ">":
                right = (barrel_r[0] + 1, barrel_r[1])
                if not self.push2(right, ">"):
                    dirty = True

                if self.get(right) == ".":
                    self.set(right, "]")
                    self.set(barrel_r, "[")
                    self.set(barrel_l, ".")
                else:
                    dirty = True

            case _:
                raise ValueError(f"unknown {direction=}")

        return not dirty
