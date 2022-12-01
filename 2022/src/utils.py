import pathlib
from typing import Callable


def read_list_of_lists(path: pathlib.Path) -> list[list]:
    """
    Read a text file and parse it as a list of lists.

    Each list item should be on it's own line, and each list ended with a blank line, eg:

    ```text
    1
    2

    3
    ```

    Would result in the output `[["1", "2"], ["3"]]`.
    """
    lists = []
    curr_list = []

    for line in path.read_text("utf-8").split("\n"):
        if not line:
            lists.append(curr_list)
            curr_list = []
        else:
            curr_list.append(line)

    if curr_list:
        lists.append(curr_list)

    return lists


def map_list_of_lists(lists: list[list], func: Callable) -> list[list]:
    """
    Apply a function to each item in each list while maintaining the existing
    'list of lists' structure.

    >>> map_list_of_lists([["1", "2"], ["3"]], int)
    [[1, 2], [3]]
    """
    return [[func(item) for item in _list] for _list in lists]


def aggregate_list_of_lists(lists: list[list], func: Callable) -> list:
    """
    Apply a function to each list, aggregating them into one list of each function's
    return value.

    >>> aggregate_list_of_lists([[1, 2], [3]], sum)
    6
    """
    return [func(_list) for _list in lists]


def find_max(things: list) -> int:
    """
    Find index of the largest thing in a list of `things`, each thing must be
    comparable to the others via `>`.

    >>> find_max([3, 2, 5, 9, 2])
    3

    >>> find_max([])
    -1
    """
    max_thing = None
    max_idx = -1

    for idx, thing in enumerate(things):
        if max_thing is None or thing > max_thing:
            max_thing = thing
            max_idx = idx

    return max_idx
