# https://old.reddit.com/r/adventofcode/comments/r9z49j/2021_day_6_solutions/hnfruss/
from functools import cache

with open("./day6/test.txt") as test:
    fish = list(map(int, test.read().split(',')))

@cache
def count_fish(life):
    if life < 0: return 1
    return count_fish(life - 7) + count_fish(life - 9)

print(sum(count_fish(79 - f) for f in fish))
print(sum(count_fish(255 - f) for f in fish))
