import math


def part_1(puzzle: str) -> int | str | float | bool:
    """Solution for AOC 2023, day 8, part 1."""
    lines = puzzle.splitlines()
    steps = list(lines[0].strip())

    graph: dict[str, tuple[str, str]] = {}
    for raw_node in lines[2:]:
        label = raw_node[0:3]
        left = raw_node[7:10]
        right = raw_node[12:15]
        graph[label] = (left, right)

    node = "AAA"
    count, idx = 0, 0
    while node != "ZZZ":
        step = steps[idx]
        node = graph[node][0] if step == "L" else graph[node][1]

        count += 1
        idx = (idx + 1) % len(steps)

    return count


def part_2(puzzle: str) -> int | str | float | bool:
    """Solution for AOC 2023, day 8, part 2."""
    lines = puzzle.splitlines()
    steps = list(lines[0].strip())

    graph: dict[str, tuple[str, str]] = {}
    for raw_node in lines[2:]:
        label = raw_node[0:3]
        left = raw_node[7:10]
        right = raw_node[12:15]
        graph[label] = (left, right)

    nodes = [n for n in graph if n.endswith("A")]
    lengths = []

    for _node in nodes:
        node = _node
        count, idx = 0, 0
        while not node.endswith("Z"):
            step = steps[idx]
            node = graph[node][0] if step == "L" else graph[node][1]

            count += 1
            idx = (idx + 1) % len(steps)
        lengths.append(count)

    return math.lcm(*lengths)
