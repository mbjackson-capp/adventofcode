from aocd import get_data
import numpy as np
import re
from itertools import combinations

# set session token first - https://github.com/wimglenn/advent-of-code-wim/issues/1

input = get_data(day=8, year=2024)


def process(input: str) -> tuple[np.array, set]:
    input_map = np.array([[char for char in row] for row in input.split("\n")])
    frequencies = sorted(list(set(re.findall(r"\w|\d", input))))
    return input_map, frequencies


def all_indices_of_frequency(map: np.array, freq: str):
    xes, ys = np.where(map == freq)
    # type-convert from np.int64
    indices_list = list(zip([int(x) for x in xes], [int(y) for y in ys]))
    return indices_list


def find_antinodes(map: np.array, pt1: tuple[int, int], pt2: tuple[int, int], part=1):
    """Find which antinodes of two antenna points, if any, exist on the map."""
    x1, y1 = pt1
    x2, y2 = pt2
    slope = (x2 - x1, y2 - y1)
    dx, dy = slope
    max_x = len(map)
    max_y = len(map[0])
    antinodes = set()
    for pt in (pt1, pt2):
        xstart, ystart = pt
        # sweep forwards and then backwards along the line from each point
        for sign in [-1, 1]:
            x = xstart
            y = ystart
            number_out = 0
            while (0 <= x < max_x) and (0 <= y < max_y):
                # in part 1 we only want the first points outward from the pair
                if part == 1 and number_out > 1:
                    break
                antinodes.add((x, y))
                x += sign * dx
                y += sign * dy
                number_out += 1
    if part == 1:
        antinodes = {an for an in antinodes if an != pt1 and an != pt2}
    return antinodes


def run(inputstr, part=1):
    antinodes = set()
    input_map, freqs = process(inputstr)
    for freq in freqs:
        all_indices = all_indices_of_frequency(input_map, freq)
        pairs = combinations(all_indices, 2)
        for pair in pairs:
            this_pair_antinodes = find_antinodes(input_map, pair[0], pair[1], part=part)
            antinodes = antinodes | this_pair_antinodes
    return len(antinodes)


print(f"Part 1 solution: {run(input)}")
print(f"Part 2 solution: {run(input, part=2)}")
