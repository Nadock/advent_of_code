"""AOC Day 17 started at 2022-12-17T17:34:33.479071+10:30"""

from typing import Optional

PIECES = [
    # Minus
    [["#", "#", "#", "#"]],
    # Plus
    [
        ["_", "#", "_"],
        ["#", "#", "#"],
        ["_", "#", "_"],
    ],
    # L
    [
        ["_", "_", "#"],
        ["_", "_", "#"],
        ["#", "#", "#"],
    ],
    # I
    [
        ["#"],
        ["#"],
        ["#"],
        ["#"],
    ],
    # Square
    [
        ["#", "#"],
        ["#", "#"],
    ],
]


def blocked(
    board: list[list[str]],
    shape: list[list[str]],
    position: tuple[int, int],
) -> bool:
    for y, row in enumerate(shape[::-1]):
        for x, cell in enumerate(row):
            if cell == "#" and board[position[1] + y][position[0] + x] == "#":
                return True
    return False


def set_pieces_height(board: list[list[str]]) -> int:
    for y, row in enumerate(board[::-1]):
        if "#" in row:
            return len(board) - y
    return 0


def set_piece(
    board: list[list[str]],
    shape: list[list[str]],
    position: tuple[int, int],
):
    for y, row in enumerate(shape[::-1]):
        for x, cell in enumerate(row):
            if cell == "#":
                board[y + position[1]][x + position[0]] = cell


def move_down(
    board: list[list[str]],
    shape: list[list[str]],
    position: tuple[int, int],
):
    new_pos = (position[0], position[1] - 1)
    if new_pos[1] < 0 or blocked(board, shape, new_pos):
        return None
    return new_pos


def print_board(
    board: list[list[str]],
    shape: Optional[list[list[str]]] = None,
    position: Optional[tuple[int, int]] = None,
) -> str:
    lines = []

    for row in board:
        row_strs = []
        for cell in row:
            row_strs.append(cell)
        lines.append(row_strs)

    if shape is not None and position is not None:
        for y, row in enumerate(shape[::-1]):
            for x, cell in enumerate(row):
                if cell == "#":
                    lines[y + position[1]][x + position[0]] = cell

    return "\n".join(["".join(line) for line in lines[::-1]])


def part_1(puzzle: str):
    """Calculates the solution to day 17's first part."""
    movements = list(puzzle.strip())
    movement_idx = 0
    board = []
    for p in range(2022):
        piece = PIECES[p % len(PIECES)]
        size = (max(len(l) for l in piece), len(piece))
        position = (2, set_pieces_height(board) + 3)

        while position[1] + size[1] >= len(board):
            board.append(["_" for _ in range(7)])

        while True:
            if movements[movement_idx % len(movements)] == ">":
                new_pos = (min(6, position[0] + 1), position[1])
                if new_pos[0] + size[0] > 6:
                    new_pos = (6 - size[0] + 1, new_pos[1])
                if not blocked(board, piece, new_pos):
                    position = new_pos
            else:
                new_pos = (max(0, position[0] - 1), position[1])
                if not blocked(board, piece, new_pos):
                    position = new_pos
            movement_idx += 1

            new_pos = move_down(board, piece, position)
            if new_pos is None:
                set_piece(board, piece, position)
                break
            position = new_pos

    return set_pieces_height(board)


def part_2(puzzle: str):
    """Calculates the solution to day 17's second part."""
    movements = list(puzzle.strip())
    movement_idx = 0
    board = []

    last_p, last_idx, last_height, skip_height = 0, 0, 0, 0

    for p in range(12073 + 1602):
        piece = PIECES[p % len(PIECES)]
        size = (max(len(l) for l in piece), len(piece))
        position = (2, set_pieces_height(board) + 3)

        while position[1] + size[1] >= len(board):
            board.append(["_" for _ in range(7)])

        while True:
            if p > 10_000 and movement_idx % len(movements) == 0:
                # print(print_board(board, piece, position))
                # print(
                #     f"{p=} (+{p-last_p}), {movement_idx=} (+{movement_idx-last_idx}), "
                #     f"{set_pieces_height(board)=} (+{set_pieces_height(board)-last_height})"
                # )

                # After this point, height increases in intervals of 10, 9, 8, 14, 12, 10
                #                                                     7, 7, 6,  8, 7,   7
                # every len(movements)
                if last_p != 0:
                    # print(
                    #     f"from here every {p-last_p} pieces increased hight by {set_pieces_height(board)-last_height}"
                    # )
                    remain = 1_000_000_000_000 - p
                    # print(f"{remain} pieces remaining -> x{remain/(p-last_p)} times")

                    times = remain // (p - last_p)
                    skip_height = set_pieces_height(board) + (
                        times * (set_pieces_height(board) - last_height)
                    )
                    # print(
                    #     f"after {times} more groups of {p-last_p} pieces the new height would be {skip_height}"
                    # )

                    # left_over = remain - (times * (p - last_p))
                    # print(f"need to simulate {left_over} more pieces")

                last_p, last_idx, last_height = (
                    p,
                    movement_idx,
                    set_pieces_height(board),
                )
            # if p > 11_000:
            #     return board

            if movements[movement_idx % len(movements)] == ">":
                new_pos = (min(6, position[0] + 1), position[1])
                if new_pos[0] + size[0] > 6:
                    new_pos = (6 - size[0] + 1, new_pos[1])
                if not blocked(board, piece, new_pos):
                    position = new_pos
            else:
                new_pos = (max(0, position[0] - 1), position[1])
                if not blocked(board, piece, new_pos):
                    position = new_pos
            movement_idx += 1

            new_pos = move_down(board, piece, position)
            if new_pos is None:
                set_piece(board, piece, position)
                break
            position = new_pos

    current_height = set_pieces_height(board)
    # print(
    #     f"{last_height=}, {current_height=}, delta={current_height-last_height}, {skip_height=}"
    # )
    return skip_height + (current_height - last_height)
