from aocd import get_data
import re
from collections import Counter

# set session token first - https://github.com/wimglenn/advent-of-code-wim/issues/1

# Problem statement: https://adventofcode.com/2024/day/1

input = get_data(day=1, year=2024).split("\n")
list_left = []
list_right = []
for line in input:
    left, right = re.split(r"\s+", line)
    list_left.append(int(left))
    list_right.append(int(right))


def part1():
    left_sorted = sorted(list_left)
    right_sorted = sorted(list_right)

    zipped = list(zip(left_sorted, right_sorted))
    diff_total = 0
    for tupl in zipped:
        l_val, r_val = tupl
        this_diff = abs(r_val - l_val)
        diff_total += this_diff
    return diff_total


def part2():
    similarity_total = 0
    right_ctr = Counter(list_right)
    for item in list_left:
        if item in right_ctr.keys():
            this_similarity = item * right_ctr[item]
            similarity_total += this_similarity
    return similarity_total


print(f"Part 1 solution: {part1()}")
print(f"Part 2 solution: {part2()}")
