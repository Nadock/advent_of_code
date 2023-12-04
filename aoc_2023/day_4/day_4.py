def part_1(puzzle: str) -> int | str | float | bool:
    """Solution for AOC 2023, day 4, part 1."""
    sum = 0

    for game in puzzle.splitlines():
        numbers = game.split(": ", 1)[1]
        ours = {
            int(n.strip())
            for n in numbers.split("|", 1)[0].split(" ")
            if n.strip() != ""
        }
        wins = {
            int(n.strip())
            for n in numbers.split("|", 1)[1].split(" ")
            if n.strip() != ""
        }

        sum += int(2 ** (len(ours.intersection(wins)) - 1))

    return sum


def part_2(puzzle: str) -> int | str | float | bool:
    """Solution for AOC 2023, day 4, part 2."""
    copies = [1 for _ in puzzle.splitlines()]
    for idx, game in enumerate(puzzle.splitlines()):
        numbers = game.split(": ", 1)[1]
        ours = {
            int(n.strip())
            for n in numbers.split("|", 1)[0].split(" ")
            if n.strip() != ""
        }
        wins = {
            int(n.strip())
            for n in numbers.split("|", 1)[1].split(" ")
            if n.strip() != ""
        }
        count = len(ours.intersection(wins))

        for j in range(idx + 1, idx + 1 + count):
            copies[j] += copies[idx]

    return sum(copies)
