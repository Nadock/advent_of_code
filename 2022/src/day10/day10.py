"""AOC Day 10 started at 2022-12-11T12:12:33.927897+10:30"""


def part1(puzzle: str):
    """Calculates the solution to day 10's first part."""
    reg_x = 1
    cycle = 1

    samples = []

    def check_reg_x():
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


def part2(puzzle: str):
    """Calculates the solution to day 10's second part."""
    sprite_pos = 1  # AKA "register X"
    cycle = 1

    pixels = []

    def check_reg_x():
        crt_pos = (cycle - 1) % 40
        if crt_pos in [sprite_pos - 1, sprite_pos, sprite_pos + 1]:
            pixels.append("#")
        else:
            pixels.append(".")

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

    return "\n".join(
        [
            "".join(pixels[:40]),
            "".join(pixels[40:80]),
            "".join(pixels[80:120]),
            "".join(pixels[120:160]),
            "".join(pixels[160:200]),
            "".join(pixels[200:240]),
        ]
    )
