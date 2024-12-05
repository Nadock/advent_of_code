def part_1(puzzle: str) -> int | str | float | bool:
    """Solution for AOC 2024, day 5, part 1."""
    rules: list[tuple[int, int]] = []

    for line in puzzle.split("\n\n", 1)[0].splitlines():
        parts = line.split("|")
        rules.append((int(parts[0]), int(parts[1])))

    sum = 0
    for update in puzzle.split("\n\n", 1)[1].splitlines():
        pages = [int(p) for p in update.split(",")]
        if is_valid(rules, pages):
            sum += pages[len(pages) // 2]

    return sum


def is_valid(rules: list[tuple[int, int]], pages: list[int]) -> bool:
    """Returns true if the `pages` are in a valid order according to the rules."""
    for idx, page in enumerate(pages):
        afters = [rule[1] for rule in rules if rule[0] == page]
        befores = [rule[0] for rule in rules if rule[1] == page]

        # Check all befores are not after current page
        for before in befores:
            if before in pages[idx + 1 :]:
                return False

        # Check all afters are not before current page
        for after in afters:
            if after in pages[0:idx]:
                return False

    return True


def part_2(puzzle: str) -> int | str | float | bool:
    """Solution for AOC 2024, day 5, part 2."""
    rules: list[tuple[int, int]] = []

    for line in puzzle.split("\n\n", 1)[0].splitlines():
        parts = line.split("|")
        rules.append((int(parts[0]), int(parts[1])))

    invalid_updates: list[list[int]] = []

    for update in puzzle.split("\n\n", 1)[1].splitlines():
        pages = [int(p) for p in update.split(",")]
        if not is_valid(rules, pages):
            invalid_updates.append(pages)

    sum = 0
    for _update in invalid_updates:
        new_order: list[int] = []
        for _page in _update:
            insert_at = len(new_order)

            for idx, np in enumerate(new_order):
                # Only one rule per any two pages, okay to just `next` the list here
                np_rule = next(r for r in rules if r in ((np, _page), (_page, np)))

                if np_rule[1] == np and insert_at > idx:
                    insert_at = idx
                if np_rule[0] == np and insert_at < idx:
                    insert_at = idx

            new_order.insert(insert_at, _page)

        sum += new_order[len(new_order) // 2]

    return sum
