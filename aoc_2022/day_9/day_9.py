"""AOC Day 9 started at 2022-12-09T21:26:52.784894+10:30"""
from __future__ import annotations

import dataclasses


@dataclasses.dataclass
class Point:
    x: int
    y: int

    history: list[tuple[int, int]] = dataclasses.field(default_factory=list)

    def __post_init__(self):
        self.history.append((self.x, self.y))

    def adjacent(self, p2: Point) -> bool:
        dx = abs(self.x - p2.x)
        dy = abs(self.y - p2.y)

        if dx in [0, 1] and dy in [0, 1]:
            return True
        return False

    def move(self, direction: str):
        if direction == "U":
            self.y += 1
        elif direction == "D":
            self.y -= 1
        elif direction == "R":
            self.x += 1
        elif direction == "L":
            self.x -= 1
        else:
            raise ValueError(f"unknown direction {direction}")

    def move_towards(self, p2: Point):
        if self.x < p2.x:
            self.move("R")
        elif self.x > p2.x:
            self.move("L")
        if self.y < p2.y:
            self.move("U")
        elif self.y > p2.y:
            self.move("D")

        self.history.append((self.x, self.y))


def part_1(puzzle: str):
    """Calculates the solution to day 9's first part."""
    head = Point(0, 0)
    tail = Point(0, 0)

    for line in puzzle.strip().splitlines():
        direction = line.split(" ")[0]
        magnitude = int(line.split(" ")[1])

        for _ in range(magnitude):
            head.move(direction)
            if not head.adjacent(tail):
                tail.move_towards(head)

    return len(set(tail.history))


def part_2(puzzle: str):
    """Calculates the solution to day 9's second part."""
    rope = [Point(0, 0) for _ in range(10)]

    for line in puzzle.strip().splitlines():
        direction = line.split(" ")[0]
        magnitude = int(line.split(" ")[1])

        for _ in range(magnitude):
            # Move the head of the rope
            rope[0].move(direction)

            # Then update each pair of points along the rope
            for idx in range(len(rope) - 1):
                head = rope[idx]
                tail = rope[idx + 1]
                if not head.adjacent(tail):
                    tail.move_towards(head)

    return len(set(rope[-1].history))
