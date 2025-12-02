def part_1(puzzle: str) -> int | str | float | bool:
    """Solution for AOC 2025, day 2, part 1."""
    ranges = [
        (int(r.split("-")[0]), int(r.split("-")[1])) for r in puzzle.strip().split(",")
    ]
    count = 0

    for start, end in ranges:
        for i in range(start, end + 1):
            id = str(i)
            if id[: len(id) // 2] == id[len(id) // 2 :]:
                count += i

    return count


def part_2(puzzle: str) -> int | str | float | bool:
    """Solution for AOC 2025, day 2, part 2."""
    ranges = [
        (int(r.split("-")[0]), int(r.split("-")[1])) for r in puzzle.strip().split(",")
    ]
    count = 0

    for start, end in ranges:
        for i in range(start, end + 1):
            id = str(i)

            for slice_len in range(1, (len(id) // 2) + 1):
                multi = len(id) // slice_len

                if id[:slice_len] * multi == id:
                    count += i
                    break

    return count
