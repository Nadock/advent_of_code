from src import utils


def part_1(puzzle: str):
    elves = utils.aggregate_list_of_lists(
        utils.map_list_of_lists(
            utils.read_list_of_lists(puzzle),
            int,
        ),
        sum,
    )
    return elves[utils.find_max(elves)]


def part_2(puzzle: str):
    elves = utils.aggregate_list_of_lists(
        utils.map_list_of_lists(
            utils.read_list_of_lists(puzzle),
            int,
        ),
        sum,
    )

    calorie_count = 0

    calorie_count += elves.pop(utils.find_max(elves))
    calorie_count += elves.pop(utils.find_max(elves))
    calorie_count += elves.pop(utils.find_max(elves))

    return calorie_count
