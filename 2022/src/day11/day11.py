"""AOC Day 11 started at 2022-12-11T19:03:18.796530+10:30"""


import dataclasses


@dataclasses.dataclass
class Monkey:
    operation: str
    test: str
    if_true: str
    if_false: str
    items: list[int] = dataclasses.field(default_factory=list)

    inspections = 0

    def do_operation(self, item: int) -> int:
        self.inspections += 1

        arg_a = self.operation.split(" ")[2]
        op = self.operation.split(" ")[3]
        arg_b = self.operation.split(" ")[4]

        if arg_a == "old":
            arg_a = item
        else:
            arg_a = int(arg_a)
        if arg_b == "old":
            arg_b = item
        else:
            arg_b = int(arg_b)

        if op == "+":
            return arg_a + arg_b
        if op == "*":
            return arg_a * arg_b
        raise ValueError(f"unknown op in monkey operation: {self.operation}")

    def do_test(self, item: int) -> bool:
        op = self.test.split(" ")[0]
        arg = self.test.split(" ")[2]
        if op == "divisible":
            return item % int(arg) == 0
        raise ValueError(f"unknown op in monkey test: {self.test}")

    def test_number(self) -> int:
        return int(self.test.split(" ")[2])

    def if_true_monkey(self) -> int:
        return int(self.if_true.replace("throw to monkey ", ""))

    def if_false_monkey(self) -> int:
        return int(self.if_false.replace("throw to monkey ", ""))


def part1(puzzle: str):
    """Calculates the solution to day 11's first part."""

    monkeys: dict[int, Monkey] = {}
    for monkey in puzzle.strip().split("\n\n"):
        lines = monkey.splitlines()
        monkeys[int(lines[0].replace("Monkey ", "").replace(":", ""))] = Monkey(
            items=[
                int(i) for i in lines[1].replace("  Starting items: ", "").split(", ")
            ],
            operation=lines[2].replace("  Operation: ", ""),
            test=lines[3].replace("  Test: ", ""),
            if_true=lines[4].replace("    If true: ", ""),
            if_false=lines[5].replace("    If false: ", ""),
        )

    for _ in range(0, 20):
        for monkey in monkeys.values():
            items = monkey.items.copy()
            monkey.items = []

            for item in items:
                item = monkey.do_operation(item)
                item //= 3
                if monkey.do_test(item):
                    monkeys[monkey.if_true_monkey()].items.append(item)
                else:
                    monkeys[monkey.if_false_monkey()].items.append(item)

    inspections = []
    for monkey in monkeys.values():
        inspections.append(monkey.inspections)

    inspections.sort(reverse=True)
    return inspections[0] * inspections[1]


def part2(puzzle: str):
    """Calculates the solution to day 11's second part."""
    monkeys: dict[int, Monkey] = {}
    for monkey in puzzle.strip().split("\n\n"):
        lines = monkey.splitlines()
        monkeys[int(lines[0].replace("Monkey ", "").replace(":", ""))] = Monkey(
            items=[
                int(i) for i in lines[1].replace("  Starting items: ", "").split(", ")
            ],
            operation=lines[2].replace("  Operation: ", ""),
            test=lines[3].replace("  Test: ", ""),
            if_true=lines[4].replace("    If true: ", ""),
            if_false=lines[5].replace("    If false: ", ""),
        )

    mod_value = 1
    for monkey in monkeys.values():
        mod_value *= monkey.test_number()

    for _ in range(0, 10_000):
        for monkey in monkeys.values():
            items = monkey.items.copy()
            monkey.items = []

            for item in items:
                item = monkey.do_operation(item)
                item %= mod_value
                if monkey.do_test(item):
                    monkeys[monkey.if_true_monkey()].items.append(item)
                else:
                    monkeys[monkey.if_false_monkey()].items.append(item)

    inspections = []
    for monkey in monkeys.values():
        inspections.append(monkey.inspections)

    inspections.sort(reverse=True)
    return inspections[0] * inspections[1]
