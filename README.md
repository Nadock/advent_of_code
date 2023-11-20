# Advent of Code

[Advent of Code](https://adventofcode.com) is a is an advent calendar of small programming puzzles. A new calendar of
puzzles is released day-by-day every December.

This repo contains my solution code for each puzzle and the my unique inputs for that puzzle. Each puzzle typically has
two parts, the first part usually being easier and the second an extension of the first.

My account on the [AoC](https://adventofcode.com) website is linked to this GitHub account.

This code is all MIT licensed, so if you would like to borrow from it you are welcome to. However, the code is not
production quality in any way so don't expect anything particularly performant, clean, beautify, etc.

## `aoc.py`

`aoc.py` is a CLI tool for automatically downloading puzzle inputs and scaffolding code files in the right structure.

### Setup

If you have never run `aoc.py` before you will need to login the the [AOC](https://adventofcode.com) website and retrieve your `session` cookie. Once you have the session cookie value, place it in a file called `cookie.txt` in the same directory as `aoc.py`.

You may have to update your `session` cookie value periodically (usually not more than once per event).

Keep this value a secret, with the `session` cookie someone could impersonate you on the AOC website!

### Directory Structure

`aoc.py` follows a consistent directory structure and file naming pattern. For example, for day `N` of year `XXXX`, the following directory structure will be created:

```console
.
├── aoc.py
└── aoc_XXXX
    └── day_N
        ├── __init__.py
        ├── day_N.py
        ├── example.txt
        └── puzzle.txt
```

`puzzle.txt` contains your individaul puzzle input for tht particular puzzle and `example.txt` contains the example input pulled from the puzzle's HTML page.

`day_N.py` contains two predefined functions `part_1` and `part_2` for each of the two parts to an AOC puzzle.

### `aoc.py init`

Run `aoc.py init` to scaffold solution files and download puzzle inputs.

```console
> aoc.py init --help

usage: aoc.py init [-h] [-y YEAR] [-d DAY] [--no-download] [--no-files] [--no-wait]

options:
  -h, --help            show this help message and exit
  -y YEAR, --year YEAR  The year of the puzzle to initialise. (default: the current year, eg: "2023")
  -d DAY, --day DAY     The day of the puzzle to initialise. (default: the current day, eg: "20")
  --no-download         Disable the automated download of the day's puzzle inputs.
  --no-files            Disable to automated creation of solution code files.
  --no-wait             Disable the automatic wait for the puzzle to become available.
```

### `aoc.py run`

Run `aoc.py run` to execute the solution code. Currently only supports years where the solution is written in Python.

```console
> aoc.py run --help

usage: aoc.py run [-h] [-y YEAR] [-d DAY] [-p {1,2}] [-i {example,puzzle}]

options:
  -h, --help            show this help message and exit
  -y YEAR, --year YEAR  The year of the puzzle to run. (default: the current year, eg: "2023")
  -d DAY, --day DAY     The day of the puzzle to run. (default: the current day, eg: "20")
  -p {1,2}, --part {1,2}
                        The part of the day's puzzle to run. (default: run both parts)
  -i {example,puzzle}, --input {example,puzzle}
                        Which input to supply to the puzzle. (default: run both inputs, example first)
```
