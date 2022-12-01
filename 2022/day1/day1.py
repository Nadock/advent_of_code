import pathlib


def part1(path: pathlib.Path):
    elves = read_elf_calories(path)
    return elves[find_max(elves)]


def part2(path: pathlib.Path):
    elves = read_elf_calories(path)

    calorie_count = 0

    calorie_count += elves.pop(find_max(elves))
    calorie_count += elves.pop(find_max(elves))
    calorie_count += elves.pop(find_max(elves))

    return calorie_count


def read_elf_calories(path: pathlib.Path) -> list[int]:
    elves = []
    elf_calories = 0

    for line in path.read_text("utf-8").split("\n"):
        if not line:
            elves.append(elf_calories)
            elf_calories = 0
        else:
            elf_calories += int(line)

    if elf_calories != 0:
        elves.append(elf_calories)

    return elves


def find_max(things: list[int]) -> int:
    """Return the index into `things` of the largest thing."""
    max_idx = 0
    max_thing = 0
    for idx, thing in enumerate(things):
        if thing > max_thing:
            max_idx = idx
            max_thing = thing

    return max_idx


if __name__ == "__main__":
    print("day1, part1, input0:", part1(pathlib.Path("./input0.txt")))
    print("day1, part1, input1 :", part1(pathlib.Path("./input1.txt")))
    print("")
    print("day1, part2, input0:", part2(pathlib.Path("./input0.txt")))
    print("day1, part2, input1 :", part2(pathlib.Path("./input1.txt")))
