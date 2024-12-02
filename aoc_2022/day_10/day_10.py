"""AOC Day 10 started at 2022-12-11T12:12:33.927897+10:30"""  # noqa: D415


def part_1(puzzle: str):  # noqa: ANN201
    """Calculates the solution to day 10's first part."""
    reg_x = 1
    cycle = 1

    samples = []

    def check_reg_x():  # noqa: ANN202
        if cycle == 20 or (cycle - 20) % 40 == 0:
            samples.append(reg_x * cycle)

    for line in puzzle.strip().splitlines():
        args = line.split(" ")

        if args[0] == "noop":
            cycle += 1
            check_reg_x()
            # No Op
        elif args[0] == "addx":
            cycle += 1
            check_reg_x()
            cycle += 1
            reg_x += int(args[1])
            check_reg_x()

    return sum(samples)


def part_2(puzzle: str):  # noqa: ANN201
    """Calculates the solution to day 10's second part."""
    sprite_pos = 1  # AKA "register X"
    cycle = 1
    pixels = [[" " for _ in range(40)] for _ in range(6)]

    def check_reg_x():  # noqa: ANN202
        row = cycle // 40
        col = (cycle - 1) % 40
        if col in [sprite_pos - 1, sprite_pos, sprite_pos + 1]:
            pixels[row][col] = "#"

    for line in puzzle.strip().splitlines():
        args = line.split(" ")

        if args[0] == "noop":
            cycle += 1
            check_reg_x()
            # No Op
        elif args[0] == "addx":
            cycle += 1
            check_reg_x()
            cycle += 1
            sprite_pos += int(args[1])
            check_reg_x()

    return "\n".join(["".join(row) for row in pixels])
