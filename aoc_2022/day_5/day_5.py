"""AOC Day 5 started at 2022-12-05T15:30:00.934665+10:30"""


class Stack:
    def __init__(self) -> None:
        self._contents = []

    def __str__(self) -> str:
        return f"Stack<{self._contents}>"

    def __repr__(self) -> str:
        return str(self)

    def push(self, item):
        self._contents.append(item)

    def pop(self):
        return self._contents.pop(-1)

    def peak(self):
        return self._contents[-1]


def part_1(puzzle: str):
    """Calculates the solution to day 5's first part."""
    crates: list[str] = []
    moves: list[str] = []
    switch = False
    for line in puzzle.splitlines():
        if not line:
            switch = True
        elif not switch:
            crates.append(line)
        else:
            moves.append(line)

    stacks: dict[str, Stack] = {}
    for idx, value in enumerate(crates[-1]):
        if value != " ":
            s = Stack()
            c = crates[:-1]
            c.reverse()
            for line in c:
                if idx < len(line) and line[idx] != " ":
                    s.push(line[idx])
            stacks[value] = s

    for move in moves:
        count = int(move.split(" ")[1])
        src = move.split(" ")[3]
        dest = move.split(" ")[5]
        for _ in range(count):
            stacks[dest].push(stacks[src].pop())

    return "".join([s.peak() for s in stacks.values()])


def part_2(puzzle: str):
    """Calculates the solution to day 5's second part."""
    crates: list[str] = []
    moves: list[str] = []
    switch = False
    for line in puzzle.splitlines():
        if not line:
            switch = True
        elif not switch:
            crates.append(line)
        else:
            moves.append(line)

    stacks: dict[str, Stack] = {}
    for idx, value in enumerate(crates[-1]):
        if value != " ":
            s = Stack()
            c = crates[:-1]
            c.reverse()
            for line in c:
                if idx < len(line) and line[idx] != " ":
                    s.push(line[idx])
            stacks[value] = s

    for move in moves:
        count = int(move.split(" ")[1])
        src = move.split(" ")[3]
        dest = move.split(" ")[5]

        src_stack = stacks[src]
        dest_stack = stacks[dest]
        items = [src_stack.pop() for _ in range(count)]
        items.reverse()
        for item in items:
            dest_stack.push(item)

    return "".join([s.peak() for s in stacks.values()])
