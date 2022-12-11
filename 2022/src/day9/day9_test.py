from urllib import request

import pytest

from src.day9 import day9


@pytest.mark.parametrize(
    "p1,p2,adjacent",
    [
        (day9.Point(1, 1), day9.Point(0, 0), True),
        (day9.Point(1, 1), day9.Point(1, 0), True),
        (day9.Point(1, 1), day9.Point(2, 0), True),
        (day9.Point(1, 1), day9.Point(3, 0), False),
        (day9.Point(1, 1), day9.Point(0, 1), True),
        (day9.Point(1, 1), day9.Point(1, 1), True),
        (day9.Point(1, 1), day9.Point(2, 1), True),
        (day9.Point(1, 1), day9.Point(3, 1), False),
        (day9.Point(1, 1), day9.Point(0, 2), True),
        (day9.Point(1, 1), day9.Point(1, 2), True),
        (day9.Point(1, 1), day9.Point(2, 2), True),
        (day9.Point(1, 1), day9.Point(3, 2), False),
    ],
)
def test_adjacent(p1: day9.Point, p2: day9.Point, adjacent: bool):
    if adjacent:
        assert p1.adjacent(p2)
        assert p2.adjacent(p1)
    else:
        assert not p1.adjacent(p2)
        assert not p2.adjacent(p1)


@pytest.mark.parametrize(
    "p1,p2,result",
    [
        (day9.Point(0, 0), day9.Point(2, 0), day9.Point(1, 0)),  # Right
        (day9.Point(2, 0), day9.Point(0, 0), day9.Point(1, 0)),  # Left
        (day9.Point(0, 0), day9.Point(0, 2), day9.Point(0, 1)),  # Down
        (day9.Point(0, 2), day9.Point(0, 0), day9.Point(0, 1)),  # Up
        (day9.Point(1, 1), day9.Point(2, 3), day9.Point(2, 2)),
        (day9.Point(1, 1), day9.Point(4, 3), day9.Point(2, 2)),
    ],
)
def test_move_towards(p1: day9.Point, p2: day9.Point, result: day9.Point):
    p1.move_towards(p2)
    assert p1.x == result.x
    assert p1.y == result.y


def test_history():
    moves = (
        ["R", "R", "R", "R"]
        + ["U", "U", "U", "U"]
        + ["L", "L", "L"]
        + ["D"]
        + ["R", "R", "R", "R"]
        + ["D"]
        + ["L", "L", "L", "L", "L"]
        + ["R", "R"]
    )
    tail_positions = (
        [(0, 0), (1, 0), (2, 0), (3, 0)]
        + [(3, 0), (4, 1), (4, 2), (4, 3)]
        + [(4, 3), (3, 4), (2, 4)]
        + [(2, 4)]
        + [(2, 4), (2, 4), (3, 3), (4, 3)]
        + [(4, 3)]
        + [(4, 3), (4, 3), (3, 2), (2, 2), (1, 2)]
        + [(1, 2), (1, 2)]
    )

    head = day9.Point(0, 0)
    tail = day9.Point(0, 0)

    for move, tail_pos in zip(moves, tail_positions, strict=True):
        head.move(move)
        if not tail.adjacent(head):
            tail.move_towards(head)

        assert (tail.x, tail.y) == tail_pos
        assert tail.history[-1] == tail_pos

    assert set(tail.history) == set(tail_positions)
