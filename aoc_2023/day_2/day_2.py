def part_1(puzzle: str) -> int | str | float | bool:
    """Solution for AOC 2023, day 2, part 1."""
    red, green, blue, sum = 12, 13, 14, 0

    for line in puzzle.splitlines():
        game_num = int(line.strip().split(":", 1)[0].replace("Game ", ""))
        possible = True

        for draws in line.strip().split(":", 1)[1].split(";"):
            for draw in draws.strip().split(", "):
                count = int(draw.split(" ", 1)[0])
                colour = draw.split(" ", 1)[1]

                if (
                    (colour == "red" and count > red)
                    or (colour == "blue" and count > blue)
                    or (colour == "green" and count > green)
                ):
                    possible = False
                    break

            if not possible:
                break

        if possible:
            sum += game_num

    return sum


def part_2(puzzle: str) -> int | str | float | bool:
    """Solution for AOC 2023, day 2, part 2."""
    sum = 0

    for line in puzzle.splitlines():
        red, green, blue = 0, 0, 0

        for draws in line.strip().split(":", 1)[1].split(";"):
            for draw in draws.strip().split(", "):
                count = int(draw.split(" ", 1)[0])
                colour = draw.split(" ", 1)[1]

                if colour == "red":
                    red = max(red, count)
                if colour == "green":
                    green = max(green, count)
                if colour == "blue":
                    blue = max(blue, count)

        sum += red * green * blue

    return sum
