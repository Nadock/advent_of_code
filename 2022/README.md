# Advent of Code — 2022

These are my solutions for the 2022 AoC calendar. Each day has it's own directory following the pattern
`:/2022/src/dayN` and two input files, one for the example on the puzzle page and the other is my unique puzzle input.

## Helper Script

I've written a quick-and-dirty helper script for this year: `aoc.py`. It has two modes, the main puzzle running mode,
and a new puzzle scaffolding mode.

### New Puzzle Scaffolding

Run `aoc.py` with the `-n` flag, for example:

```console
> pipenv run ./aoc.py -n 1

Scaffolded day 1 files...
Retrieved puzzle inputs for day 1...
Day 1 is ready to be solved in:
/Users/riley.chase/repos/advent_of_code/2022/src/day1
```

This will create the puzzle directory in the correct location (ie: `:/2022/src/day1`), add the empty `.py` files and
input files, then it will download the input content from the AOC site.

To access the AOC site, you will need to put your session cookie in the `:/2022/.session_cookie` file.

### Puzzle Execution

To run the code for a puzzle, you tell `aoc.py` which day, part, and input you would like to run. For example, to run
day 3, part 1, input 0 you would run:

```console
> pipenv run ./aoc.py 3 1 0

Solution for day 3, part 1, input 0:
157
```

The `aoc.py` script will dynamically import the correct day's solution file and run the corresponding puzzle function
and print whatever is returned to stdout.
