"""AOC Day 12 started at 2022-12-12T16:40:48.912598+10:30"""
from __future__ import annotations

import dataclasses
from typing import Optional


@dataclasses.dataclass
class Node:
    height: int
    end: bool = False
    children: list[Node] = dataclasses.field(default_factory=list)

    parent: Optional[Node] = None
    seen: bool = False


def part_1(puzzle: str):
    """Calculates the solution to day 12's first part."""
    # Convert input into graph nodes
    grid: list[list[Node]] = []
    start = None
    for line in puzzle.strip().splitlines():
        row = []
        for char in line:
            node = Node(height=ord(char) - ord("a"))
            row.append(node)

            if char == "S":
                start = node
                node.height = 0
            elif char == "E":
                node.height = ord("z") - ord("a")
                node.end = True

        grid.append(row)

    if start is None:
        raise ValueError(f"did not find {start=} node")

    # Link nodes that are adjacent in the grid and have low enough heigh difference
    for x, row in enumerate(grid):
        for y, node in enumerate(row):
            for adj_x, adj_y in [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]:
                if (
                    adj_x >= 0
                    and adj_x < len(grid)
                    and adj_y >= 0
                    and adj_y < len(grid[adj_x])
                ):
                    adj_node = grid[adj_x][adj_y]
                    if node.height >= adj_node.height - 1:
                        node.children.append(adj_node)

    # Can now ignore the rest of the grid and BFS to the target
    _end = bfs(start)
    path = [_end]
    node = _end.parent
    while node is not start and node is not None:
        path.append(node)
        node = node.parent
    return len(path)


def bfs(start: Node) -> Node:
    queue = [start]
    start.seen = True

    while len(queue) != 0:
        node = queue.pop(0)
        if node.end:
            return node

        for child in node.children:
            if not child.seen:
                child.seen = True
                child.parent = node
                queue.append(child)

    raise ValueError("no path to end node")


def part_2(puzzle: str):
    """Calculates the solution to day 12's second part."""
    # Convert input into graph nodes
    grid: list[list[Node]] = []
    for line in puzzle.strip().splitlines():
        row = []
        for char in line:
            node = Node(height=ord(char) - ord("a"))
            row.append(node)

            if char == "S":
                node.height = 0
            elif char == "E":
                node.height = ord("z") - ord("a")
                node.end = True

        grid.append(row)

    # Link nodes that are adjacent in the grid and have low enough heigh difference
    starts = []
    for x, row in enumerate(grid):
        for y, node in enumerate(row):
            if node.height == 0:
                starts.append(node)

            for adj_x, adj_y in [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]:
                if (
                    adj_x >= 0
                    and adj_x < len(grid)
                    and adj_y >= 0
                    and adj_y < len(grid[adj_x])
                ):
                    adj_node = grid[adj_x][adj_y]
                    if node.height >= adj_node.height - 1:
                        node.children.append(adj_node)

    # Can now ignore the rest of the grid and BFS to the target
    min_path = None
    for node in starts:
        try:
            end = bfs(node)
        except ValueError:
            continue

        count = 0
        while end is not None and end.height != 0:
            count += 1
            end = end.parent

        if min_path is None or count < min_path:
            min_path = count

        for row in grid:
            for node in row:
                node.parent = None
                node.seen = False

    return min_path
