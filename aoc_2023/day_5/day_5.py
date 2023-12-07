import functools
import multiprocessing


def part_1(puzzle: str) -> int | str | float | bool:
    """Solution for AOC 2023, day 5, part 1."""
    lines = puzzle.splitlines()

    seeds = [int(s) for s in lines[0].split("seeds: ", 1)[1].split()]
    maps = []

    current_map: list[tuple[int, int, int]] = []
    for line in lines[2:]:
        if line.endswith("map:"):
            pass
        elif line == "":
            maps.append(current_map)
            current_map = []
        else:
            dest_start = int(line.split()[0])
            source_start = int(line.split()[1])
            width = int(line.split()[2])
            current_map.append((dest_start, source_start, width))
    if current_map:
        maps.append(current_map)

    min = None

    for seed in seeds:
        value = convert(maps, seed)
        if min is None or value < min:
            min = value

    if min is None:
        raise ValueError("did not find a min seed")

    return min


def convert_via_map(map: list[tuple[int, int, int]], value: int) -> int:
    for dest, source, width in map:
        if value >= source and value <= source + width:
            offset = value - source
            return dest + offset
    return value


def convert(maps: list[list[tuple[int, int, int]]], value: int) -> int:
    for map in maps:
        value = convert_via_map(map, value)
    return value


def part_2(puzzle: str) -> int | str | float | bool:
    """Solution for AOC 2023, day 5, part 2."""
    lines = puzzle.splitlines()

    maps = []
    map: list[tuple[int, int, int]] = []
    for line in lines[2:]:
        if line.endswith("map:"):
            pass
        elif line == "":
            maps.append(map)
            map = []
        else:
            dest_start = int(line.split()[0])
            source_start = int(line.split()[1])
            width = int(line.split()[2])
            map.append((dest_start, source_start, width))
    maps.append(map)

    _seeds = lines[0].split("seeds: ", 1)[1].split()
    ranges = []
    for idx in range(0, len(_seeds), 2):
        seed = int(_seeds[idx])
        width = int(_seeds[idx + 1])
        ranges.append((seed, seed + width))

    s_min = None

    with multiprocessing.Pool() as p:
        for r in ranges:
            _r = list(range(r[0], r[1]))
            print(f"{r=} => {r[1]-r[0]}, {s_min=}")
            values = p.map(functools.partial(convert, maps), _r)
            s_min = min(values) if s_min is None else min(s_min, *values)

    return s_min


def merge_ranges(ranges: list[tuple[int, int]]) -> tuple[int, int]:
    ranges.sort(key=lambda r: r[0])
    a = ranges[0]
    for b in ranges[1:]:
        a = merge_range(a, b)
    return a


def merge_range(a: tuple[int, int], b: tuple[int, int]) -> tuple[int, int]:
    # a    a
    #   b    b
    if a[0] <= b[0] and b[1] >= a[1]:
        return (min(a[0], b[0]), max(a[1], b[1]))

    #   a    a
    # b    b
    if a[0] >= b[0] and b[1] <= a[1]:
        return (min(a[0], b[0]), max(a[1], b[1]))

    raise ValueError(f"no overlap between ranges {a=} & {b=}")
