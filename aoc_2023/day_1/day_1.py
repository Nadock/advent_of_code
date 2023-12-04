import contextlib


def part_1(puzzle: str) -> int | str | float | bool:
    """Solution for AOC 2023, day 1, part 1."""
    sum = 0
    for line in puzzle.splitlines():
        first_num, last_num = 0, 0

        for char in line.strip():
            with contextlib.suppress(ValueError):
                first_num = int(char)
                break

        for char in line.strip()[::-1]:
            with contextlib.suppress(ValueError):
                last_num = int(char)
                break

        sum += int(f"{first_num}{last_num}")

    return sum


def part_2(puzzle: str) -> int | str | float | bool:
    """Solution for AOC 2023, day 1, part 2."""
    sum = 0
    for line in puzzle.splitlines():
        first = find_first_num(line)
        last = find_first_num(line, reverse=True)
        sum += int(f"{first}{last}")
    return sum


def find_first_num(s: str, reverse: bool = False) -> int:
    """
    Finds the first digit or digit word in a string, reading either forwards or reverse.
    """
    words = {
        "one": 1,
        "two": 2,
        "three": 3,
        "four": 4,
        "five": 5,
        "six": 6,
        "seven": 7,
        "eight": 8,
        "nine": 9,
    }

    s = s[::-1] if reverse else s

    #  i   j
    #  |   |
    # "thisstring"

    for j, char in enumerate(s):
        with contextlib.suppress(ValueError):
            return int(char)

        for i in range(j):
            word = "".join(s[i : j + 1][::-1]) if reverse else "".join(s[i : j + 1])
            if word in words:
                return words[word]

    raise ValueError(f"no number in {s=}")
