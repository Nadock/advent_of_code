import collections
import string


def part_1(puzzle: str) -> int | str | float | bool:
    """Solution for AOC 2023, day 3, part 1."""
    schematic = [list(line.strip()) for line in puzzle.strip().splitlines()]
    sum = 0

    for row_idx, row in enumerate(schematic):
        start, end = None, None

        for col_idx, symbol in enumerate(row):
            if symbol in string.digits and start is None:
                start = col_idx
            if symbol not in string.digits and start is not None:
                end = col_idx
            if end is None and start is not None and col_idx + 1 == len(row):
                end = len(row)

            if start is not None and end is not None:
                num = int("".join(row[start:end]))

                up = max(row_idx - 1, 0)
                down = min(row_idx + 2, len(schematic))
                left = max(start - 1, 0)
                right = min(end + 1, len(row))

                sub_schema = [row[left:right] for row in schematic[up:down]]

                symbol_adjacent = False
                for sub_row in sub_schema:
                    for sub_symbol in sub_row:
                        if sub_symbol != "." and sub_symbol not in string.digits:
                            symbol_adjacent = True
                            break
                    if symbol_adjacent:
                        break

                if symbol_adjacent:
                    sum += num

                start, end = None, None

    return sum


def part_2(puzzle: str) -> int | str | float | bool:
    """Solution for AOC 2023, day 3, part 2."""
    schematic = [list(line.strip()) for line in puzzle.strip().splitlines()]
    gears: dict[tuple[int, int], list[int]] = collections.defaultdict(list)
    sum = 0

    for row_idx, row in enumerate(schematic):
        start, end = None, None

        for col_idx, symbol in enumerate(row):
            if symbol in string.digits and start is None:
                start = col_idx
            if symbol not in string.digits and start is not None:
                end = col_idx
            if end is None and start is not None and col_idx + 1 == len(row):
                end = len(row)

            if start is not None and end is not None:
                num = int("".join(row[start:end]))

                up = max(row_idx - 1, 0)
                down = min(row_idx + 2, len(schematic))
                left = max(start - 1, 0)
                right = min(end + 1, len(row))

                for sub_row_idx in range(up, down):
                    for sub_col_idx in range(left, right):
                        if schematic[sub_row_idx][sub_col_idx] == "*":
                            gears[(sub_row_idx, sub_col_idx)].append(num)

                start, end = None, None

    for ratios in gears.values():
        if len(ratios) == 2:
            sum += ratios[0] * ratios[1]

    return sum
