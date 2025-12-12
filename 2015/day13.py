from aocd import get_data
from itertools import permutations
from tqdm import tqdm

# set session token first - https://github.com/wimglenn/advent-of-code-wim/issues/1

input = get_data(day=13, year=2015)


def parse_input(data: str):
    lines = data.split("\n")
    happinesses = {}
    for line in lines:
        line = line.split(" ")
        name = line[0]
        change = -int(line[3]) if line[2] == "lose" else int(line[3])
        next_to = line[-1][:-1]
        if name not in happinesses:
            happinesses[name] = {}
        happinesses[name][next_to] = change
    guests = list(happinesses.keys())
    return guests, happinesses


def optimal_happiness_change(data: str, part=1) -> int:
    """NOTE: provided input indicates (8-1)! = 5040 possible seating arrangements,
    per formula that there are (n-1)! cyclic permutations of n objects.
    Beware that this could take much longer for larger inputs."""
    guests, happinesses = parse_input(data)
    if part == 2:
        guests.append("You")
        happinesses["You"] = {}
        for g in guests:
            happinesses["You"][g] = 0
            happinesses[g]["You"] = 0
    max_change = 0
    # TODO: get rid of the redundant permutations given cyclicality
    for p in tqdm(list(permutations(guests))):
        this_change = 0
        for i, guest in enumerate(p):
            this_change += happinesses[guest][p[(i + 1) % len(p)]]
            this_change += happinesses[guest][p[(i - 1) % len(p)]]
        if this_change > max_change:
            max_change = this_change
    return max_change


if __name__ == "__main__":
    print(f"Part 1 answer: {optimal_happiness_change(input)}")
    print(f"Part 2 answer: {optimal_happiness_change(input, part=2)}")
