"""AOC Day 7 started at 2022-12-07T15:30:05.691237+10:30"""  # noqa: D415

from __future__ import annotations

import dataclasses

MAX_DIR_SIZE = 100_000
FS_MAX_SIZE = 70_000_000
UPDATE_SIZE = 30_000_000


@dataclasses.dataclass
class Directory:  # noqa: D101
    name: str
    parent: Directory | None
    children: dict[str, Directory] = dataclasses.field(default_factory=dict)
    files: dict[str, int] = dataclasses.field(default_factory=dict)

    def cd(self, path) -> Directory:  # noqa: ANN001, D102
        if path == "/":
            raise ValueError("cannot cd to root")

        if path == "..":
            if self.parent is None:
                return self
            return self.parent

        return self.children[path]

    def size(self) -> int:  # noqa: D102
        size = 0
        for child in self.children.values():
            size += child.size()
        for file in self.files.values():
            size += file
        return size

    def iter_dirs(self):  # noqa: ANN201, D102
        for child in self.children.values():
            for child_dir in child.iter_dirs():  # noqa: UP028
                yield child_dir
            yield child


def parse_cmds(root: Directory, lines: list[str]):  # noqa: ANN201, D103
    pwd = root

    for idx, line in enumerate(lines):
        args = line.split(" ")
        if args[0] != "$":
            continue

        if args[1] == "cd":
            path = args[2]
            if path == "/":  # noqa: SIM108
                pwd = root
            else:
                pwd = pwd.cd(path)
        else:
            for ls_line in lines[idx + 1 :]:
                args = ls_line.split(" ")
                if args[0] == "$":
                    break
                size_or_dir = args[0]
                name = args[1]
                if size_or_dir == "dir":
                    pwd.children.setdefault(name, Directory(name=name, parent=pwd))
                else:
                    pwd.files[name] = int(size_or_dir)


def part_1(puzzle: str):  # noqa: ANN201
    """Calculates the solution to day 7's first part."""
    lines = puzzle.strip().splitlines()
    root = Directory(name="/", parent=None)
    parse_cmds(root, lines)

    s = 0
    for child_dir in root.iter_dirs():
        if child_dir.size() <= MAX_DIR_SIZE:
            s += child_dir.size()

    return s


def part_2(puzzle: str):  # noqa: ANN201
    """Calculates the solution to day 7's second part."""
    lines = puzzle.strip().splitlines()
    root = Directory(name="/", parent=None)
    parse_cmds(root, lines)

    free_space = FS_MAX_SIZE - root.size()

    potential_deletes = [
        c for c in root.iter_dirs() if c.size() + free_space >= UPDATE_SIZE
    ]

    min_dir = root
    for child_dir in potential_deletes:
        if child_dir.size() <= min_dir.size():
            min_dir = child_dir

    return min_dir.size()
