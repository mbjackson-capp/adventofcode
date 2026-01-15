from aocd import get_data
from typing import List
import re

# set session token first - https://github.com/wimglenn/advent-of-code-wim/issues/1

# Problem statement: https://adventofcode.com/2018/day/3

# Do this the other way. Keep a big dict of points and make the value of each
# a set/list of claims that it is in.

test_input = """#1 @ 1,3: 4x4
#2 @ 3,1: 4x4
#3 @ 5,5: 2x2""".split(
    "\n"
)


def parse_claim(claim):
    """Convert a claim string into a set of points that it covers, plus its id"""
    claim_id, in_left, in_top, width, height = [
        int(i) for i in re.split(r":?\s@?\s?|,|x", claim[1:])
    ]
    point_set = set()
    for h in range(in_top, in_top + height):
        for w in range(in_left, in_left + width):
            point = (h, w)
            point_set.add(point)
    return claim_id, point_set


def plot_claims(data: List[str]) -> dict:
    all_points = {}
    for claim in data:
        id, point_set = parse_claim(claim)
        for point in point_set:
            if point not in all_points:
                all_points[point] = id
            else:
                all_points[point] = "X"
    return all_points


def part1(data: List[str]) -> int:
    plot = plot_claims(data)
    return len([k for k, v in plot.items() if v == "X"])


def part2(data: List[str]) -> int:
    plot = plot_claims(data)
    for claim in data:
        id, point_set = parse_claim(claim)
        overlap_count = len({pt for pt in point_set if plot[pt] == "X"})
        if overlap_count == 0:
            return id


if __name__ == "__main__":
    input = get_data(day=3, year=2018).split("\n")
    print(f"Part 1 answer: {part1(input)}")
    print(f"Part 2 answer: {part2(input)}")
