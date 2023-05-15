from aocd import get_data
#set session token first - https://github.com/wimglenn/advent-of-code-wim/issues/1
import re

#Problem statement: https://adventofcode.com/2022/day/4

input = [re.split(r'-|,', i) for i in get_data(day=4, year=2022).split('\n')]
input = [[int(i) for i in j] for j in input]

def part1():
    total = 0
    for assignment in input:
        lb1, ub1, lb2, ub2 = assignment
        if (lb1 <= lb2 and ub1 >= ub2) or (lb2 <= lb1 and ub2 >= ub1):
            total += 1
    return total

def part2():
    total = 0
    for assignment in input:
        lb1, ub1, lb2, ub2 = assignment
        if (ub1 >= lb2) and (ub2 >= lb1):
            total += 1
    return total

print(f"Part 1 answer: {part1()}")
print(f"Part 2 answer: {part2()}")