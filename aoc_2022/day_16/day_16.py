"""
AOC Day 16 started at 2022-12-16T15:30:03.729946+10:30

Full transparency this puzzle got me good, had to research how others were doing it.
This is basically a direct recreation of the solution described here:
https://old.reddit.com/r/adventofcode/comments/zn6k1l/2022_day_16_solutions/j0ftnif/
"""  # noqa: D415

import collections


class IDMap:  # noqa: D101
    def __init__(self) -> None:
        self.max = 0
        self.map = {}

    def add(self, value) -> int:  # noqa: ANN001, D102
        if value not in self.map:
            self.map[value] = self.max
            self.max += 1
        return self.map[value]


def part_1(puzzle: str):  # noqa: ANN201
    """Calculates the solution to day 16's first part."""
    valves = []
    valve_ids = IDMap()
    for line in puzzle.strip().splitlines():
        # 0     1  2   3    4       5       6    7  8      9...
        # Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
        splits = line.split(" ")
        valve = (
            splits[1],
            int(splits[4].removeprefix("rate=").removesuffix(";")),
            [v.replace(",", "") for v in splits[9:]],
        )
        valves.append(valve)
        valve_ids.add(valve[0])

    max_n = 128
    flow_rates = [0] * max_n
    graph = [[max_n + 10] * max_n for _ in range(max_n)]
    for i in range(max_n):
        graph[i][i] = 0
    pos_rate_valves = []
    for name, rate, edges in valves:
        flow_rates[valve_ids.map[name]] = rate
        if rate > 0 or name == "AA":
            pos_rate_valves.append(valve_ids.map[name])
        for adj_valve in edges:
            graph[valve_ids.map[name]][valve_ids.map[adj_valve]] = min(
                graph[valve_ids.map[name]][valve_ids.map[adj_valve]],
                1,
            )

    for i in range(valve_ids.max):
        for j in range(valve_ids.max):
            for k in range(valve_ids.max):
                graph[j][k] = min(graph[j][k], graph[j][i] + graph[i][k])

    def simulate(time):  # noqa: ANN001, ANN202
        queue = collections.deque()
        best = collections.defaultdict(lambda: -1)

        aa = pos_rate_valves.index(valve_ids.map["AA"])

        def add(i, added, v, t):  # noqa: ANN001, ANN202
            if t >= 0 and (best[(i, added, t)] < v):
                best[(i, added, t)] = v
                queue.append((i, t, added, v))

        add(aa, 0, 0, time)
        while queue:
            i, t, added, v = queue.popleft()
            if (added & (1 << i)) == 0 and t >= 1:
                flow_here = (t - 1) * flow_rates[pos_rate_valves[i]]
                add(i, added | (1 << i), v + flow_here, t - 1)

            for j in range(len(pos_rate_valves)):
                t_move = graph[pos_rate_valves[i]][pos_rate_valves[j]]
                if t_move <= t:
                    add(j, added, v, t - t_move)

        return best

    best = simulate(30)
    return max(best.values())


def part_2(puzzle: str):  # noqa: ANN201
    """Calculates the solution to day 16's second part."""
    valves = []
    valve_ids = IDMap()
    for line in puzzle.strip().splitlines():
        # 0     1  2   3    4       5       6    7  8      9...
        # Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
        splits = line.split(" ")
        valve = (
            splits[1],
            int(splits[4].removeprefix("rate=").removesuffix(";")),
            [v.replace(",", "") for v in splits[9:]],
        )
        valves.append(valve)
        valve_ids.add(valve[0])

    max_n = 128
    flow_rates = [0] * max_n
    graph = [[max_n + 10] * max_n for _ in range(max_n)]
    for i in range(max_n):
        graph[i][i] = 0
    pos_rate_valves = []
    for name, rate, edges in valves:
        flow_rates[valve_ids.map[name]] = rate
        if rate > 0 or name == "AA":
            pos_rate_valves.append(valve_ids.map[name])
        for adj_valve in edges:
            graph[valve_ids.map[name]][valve_ids.map[adj_valve]] = min(
                graph[valve_ids.map[name]][valve_ids.map[adj_valve]],
                1,
            )

    for i in range(valve_ids.max):
        for j in range(valve_ids.max):
            for k in range(valve_ids.max):
                graph[j][k] = min(graph[j][k], graph[j][i] + graph[i][k])

    def simulate(time):  # noqa: ANN001, ANN202
        queue = collections.deque()
        best = collections.defaultdict(lambda: -1)

        aa = pos_rate_valves.index(valve_ids.map["AA"])

        def add(i, added, v, t):  # noqa: ANN001, ANN202
            if t >= 0 and (best[(i, added, t)] < v):
                best[(i, added, t)] = v
                queue.append((i, t, added, v))

        add(aa, 0, 0, time)
        while queue:
            i, t, added, v = queue.popleft()
            if (added & (1 << i)) == 0 and t >= 1:
                flow_here = (t - 1) * flow_rates[pos_rate_valves[i]]
                add(i, added | (1 << i), v + flow_here, t - 1)

            for j in range(len(pos_rate_valves)):
                t_move = graph[pos_rate_valves[i]][pos_rate_valves[j]]
                if t_move <= t:
                    add(j, added, v, t - t_move)

        return best

    best = simulate(26)
    # best => (end_node, mask_turned, time_left) => max_flow
    table = [0] * (1 << len(pos_rate_valves))
    for (i, added, t), vmax in best.items():  # noqa: B007
        table[added] = max(table[added], vmax)

    result = 0
    for mask in range(1 << len(pos_rate_valves)):
        mask2 = ((1 << len(pos_rate_valves)) - 1) ^ mask
        result = max(result, table[mask2])
        mask3 = mask
        while mask3 > 0:
            result = max(result, table[mask2] + table[mask3])
            mask3 = (mask3 - 1) & mask

    return result
