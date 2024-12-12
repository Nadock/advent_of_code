def part_1(puzzle: str) -> int | str | float | bool:
    """Solution for AOC 2024, day 9, part 1."""
    drive: list[str] = []
    free_idx = -1
    file_idx = 0
    for idx, char in enumerate(puzzle.strip()):
        if idx % 2 == 0:
            if not drive:
                free_idx = int(char)
            drive.extend([str(file_idx) for _ in range(int(char))])
            file_idx += 1
        else:
            drive.extend(["." for _ in range(int(char))])

    file_idx = len(drive) - 1

    while file_idx > 0 and free_idx < len(drive) and file_idx > free_idx:
        drive[free_idx] = drive[file_idx]
        drive[file_idx] = "."

        file_idx -= 1
        while file_idx >= 0 and drive[file_idx] == ".":
            file_idx -= 1

        free_idx += 1
        while free_idx < len(drive) and drive[free_idx] != ".":
            free_idx += 1

    check = 0
    for idx, char in enumerate(drive):
        if char == ".":
            break
        check += idx * int(char)

    return check


def part_2(puzzle: str) -> int | str | float | bool:
    """Solution for AOC 2024, day 9, part 2."""
    drive: list[str] = []
    file_idx = 0
    file_lengths = {}
    for idx, char in enumerate(puzzle.strip()):
        if idx % 2 == 0:
            drive.extend([str(file_idx) for _ in range(int(char))])
            file_lengths[str(file_idx)] = int(char)
            file_idx += 1
        else:
            drive.extend(["." for _ in range(int(char))])
    file_idx = len(drive) - 1

    free_space = find_freespace(drive)

    while file_idx >= 0:
        file_len = file_lengths[drive[file_idx]]
        free_idx = find_free(free_space, file_len, file_idx)

        if free_idx >= 0:
            free_space = update_freespace(free_space, free_idx, file_len)
            for _ in range(file_len):
                drive[free_idx] = drive[file_idx]
                drive[file_idx] = "."
                file_idx -= 1
                free_idx += 1
        else:
            file_idx -= file_len
        while file_idx >= 0 and drive[file_idx] == ".":
            file_idx -= 1

    check = 0
    for idx, char in enumerate(drive):
        if char == ".":
            continue
        check += idx * int(char)

    return check


def find_free(free: list[tuple[int, int]], size: int, stop: int) -> int:
    """Find a free space of at least `size` with index less than `stop`."""
    for idx, space in free:
        if idx > stop:
            continue
        if space >= size:
            return idx
    return -1


def find_freespace(drive: list[str]) -> list[tuple[int, int]]:
    """Find all of the free space in pairs of (start_idx, size)."""
    idx = 0
    free = []
    while idx < len(drive):
        if drive[idx] == ".":
            count = 0
            for c in drive[idx:]:
                if c != ".":
                    break
                count += 1
            free.append((idx, count))
            idx += count
        else:
            idx += 1
    free.sort(key=lambda s: s[0])
    return free


def update_freespace(
    free: list[tuple[int, int]], idx: int, len: int
) -> list[tuple[int, int]]:
    """Update the free space list by removing `len` from the free space at `idx`."""
    del_idx = -1
    for i, space in enumerate(free):
        if space[0] == idx:
            del_idx = i
            break
    old = free.pop(del_idx)
    if old[1] > len:
        free.append((old[0] + len, old[1] - len))
    free.sort(key=lambda s: s[0])
    return free
