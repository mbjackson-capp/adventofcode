from aocd import get_data
from functools import reduce

# set session token first - https://github.com/wimglenn/advent-of-code-wim/issues/1

input = get_data(day=3, year=2020).split("\n")
input = [[chr for chr in line] for line in input]  # create 2d array

WRAP_INDEX = len(input[0])
SLOPES = [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]
tree_counts = []

for slope in SLOPES:
    dx = slope[0]
    dy = slope[1]
    tree_count = 0
    curr_x = 0
    for i in range(dy, len(input), dy):
        curr_x = (curr_x + dx) % WRAP_INDEX
        if input[i][curr_x] == "#":
            tree_count += 1
    tree_counts.append(tree_count)

print(f"Part 1 solution: {tree_counts[1]}")
print(f"Part 2 solution: {reduce(lambda x, y: x * y, tree_counts)}")
