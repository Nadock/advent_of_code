import collections
import functools


def part_1(puzzle: str) -> int | str | float | bool:
    """Solution for AOC 2023, day 7, part 1."""
    games = [(line.split()[0], int(line.split()[1])) for line in puzzle.splitlines()]

    games.sort(
        key=functools.cmp_to_key(lambda a, b: compare_hands_1(a[0], b[0])),
        reverse=True,
    )

    sum = 0
    for idx, game in enumerate(games):
        sum += (idx + 1) * game[1]

    return sum


card_rank_1 = ["A", "K", "Q", "J", "T", "9", "8", "7", "6", "5", "4", "3", "2"]
card_rank_2 = ["A", "K", "Q", "T", "9", "8", "7", "6", "5", "4", "3", "2", "J"]


def compare_hands_1(a: str, b: str) -> int:  # noqa: D103
    type_a, type_b = hand_type_1(a), hand_type_1(b)

    if type_a > type_b:
        return -1
    if type_a < type_b:
        return 1

    for card_a, card_b in zip(a, b, strict=True):
        rank_a, rank_b = card_rank_1.index(card_a), card_rank_1.index(card_b)

        if rank_a < rank_b:
            return -1
        if rank_a > rank_b:
            return 1

    return 0


def hand_type_1(hand: str) -> int:  # noqa: D103, PLR0911
    cards = list(hand)

    counts_dict: dict[str, int] = collections.defaultdict(lambda: 0)
    for card in cards:
        counts_dict[card] += 1
    counts_list = list(counts_dict.values())
    if len(cards) != 5 or sum(counts_list) != 5:
        raise ValueError(f"unknown hand type: {hand=}, {cards=}, {counts_dict=}")

    # Five of a kind
    if len(counts_list) == 1:
        return 6
    # Four of a kind
    if len(counts_list) == 2 and 4 in counts_list:
        return 5
    # Full house
    if len(counts_list) == 2 and 3 in counts_list and 2 in counts_list:
        return 4
    # Three of a kind
    if len(counts_list) == 3 and 3 in counts_list and 1 in counts_list:
        return 3
    # Two pair
    if len(counts_list) == 3 and 2 in counts_list and 1 in counts_list:
        return 2
    # One pair
    if len(counts_list) == 4 and 2 in counts_list and 1 in counts_list:
        return 1
    # High card
    if len(counts_list) == 5:
        return 0

    raise ValueError(f"unknown hand type: {hand=}, {cards=}, {counts_dict=}")


def part_2(puzzle: str) -> int | str | float | bool:
    """Solution for AOC 2023, day 7, part 2."""
    games = [(line.split()[0], int(line.split()[1])) for line in puzzle.splitlines()]

    games.sort(
        key=functools.cmp_to_key(lambda a, b: compare_hands_2(a[0], b[0])),
        reverse=True,
    )

    sum = 0
    for idx, game in enumerate(games):
        sum += (idx + 1) * game[1]
    return sum


def hand_type_2(hand: str) -> int:  # noqa: D103
    h_type = hand_type_1(hand)

    if "J" not in hand:
        return h_type

    for card in card_rank_2:
        h_type = max(h_type, hand_type_1(hand.replace("J", card)))

    return h_type


def compare_hands_2(a: str, b: str) -> int:  # noqa: D103
    type_a, type_b = hand_type_2(a), hand_type_2(b)

    if type_a > type_b:
        return -1
    if type_a < type_b:
        return 1

    for card_a, card_b in zip(a, b, strict=True):
        rank_a, rank_b = card_rank_2.index(card_a), card_rank_2.index(card_b)

        if rank_a < rank_b:
            return -1
        if rank_a > rank_b:
            return 1

    return 0
