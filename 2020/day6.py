from aocd import get_data
import re
from functools import reduce

# set session token first - https://github.com/wimglenn/advent-of-code-wim/issues/1

input = get_data(day=6, year=2020)
# separate out each respondent group
input = re.sub("\n\n", "|", input)
input = re.sub("\n", " ", input)
input = re.split(r"\|", input)
input = [re.split(" ", group) for group in input]

part1_total = 0
part2_total = 0
for group in input:
    sets = [set([char for char in person]) for person in group]
    this_part1 = len(reduce(lambda x, y: x.union(y), sets))
    part1_total += this_part1
    this_part2 = len(reduce(lambda x, y: x.intersection(y), sets))
    part2_total += this_part2

print(f"Part 1 solution: {part1_total}")
print(f"Part 2 solution: {part2_total}")
