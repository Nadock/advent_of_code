import pathlib
from typing import Optional

# Convert encoded instructions to RPS
_rps_syntax = {
    "A": "rock",
    "B": "paper",
    "C": "scissors",
    "X": "rock",
    "Y": "paper",
    "Z": "scissors",
}

# Score a choice of action
_rps_score = {
    "rock": 1,
    "paper": 2,
    "scissors": 3,
}

# If the opponent has key we choose value to lose
_lose = {
    "rock": "scissors",
    "paper": "rock",
    "scissors": "paper",
}

# If the opponent has key we choose value to win
_win = {
    "rock": "paper",
    "paper": "scissors",
    "scissors": "rock",
}


def _score_rps(us: str, them: str) -> int:
    """Score an RPS game for us."""
    score = _rps_score[us]
    win = _win_rps(us, them)
    if win is None:
        score += 3
    elif win:
        score += 6
    return score


def _win_rps(us: str, them: str) -> Optional[bool]:
    """Return true if `a` beats `b` in RPS, or `None` if tied."""
    if (
        (us == "rock" and them == "scissors")
        or (us == "paper" and them == "rock")
        or (us == "scissors" and them == "paper")
    ):
        return True

    if (
        (us == "rock" and them == "paper")
        or (us == "paper" and them == "scissors")
        or (us == "scissors" and them == "rock")
    ):
        return False

    return None


def part1(path: pathlib.Path):
    """Calculates the solution to day 2's first part."""
    score = 0
    for line in path.read_text("utf-8").split("\n"):
        if line:
            them = _rps_syntax[line.split(" ")[0]]
            us = _rps_syntax[line.split(" ")[1]]
            score += _score_rps(us, them)
    return score


def part2(path: pathlib.Path):
    """Calculates the solution to day 2's second part."""
    score = 0
    for line in path.read_text("utf-8").split("\n"):
        if line:
            them = _rps_syntax[line.split(" ")[0]]

            if line.split(" ")[1] == "X":
                us = _lose[them]
            elif line.split(" ")[1] == "Y":
                us = them
            else:
                us = _win[them]

            score += _score_rps(us, them)
    return score
