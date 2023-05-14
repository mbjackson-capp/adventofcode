from aocd import get_data
#set session token first - https://github.com/wimglenn/advent-of-code-wim/issues/1
import re

#Problem statement: https://adventofcode.com/2022/day/3

input = get_data(day=3, year=2022).split('\n')

def priority(char):
    if re.match(r'[a-z]', char):
        return ord(char) - ord('a') + 1 #range 1 through 26 for a-z
    elif re.match(r'[A-Z]', char):
        return ord(char) - ord('A') + 27 #range 27 through 52 for A-Z

def part1():
    priority_sum = 0
    for rucksack in input:
        halfway = len(rucksack) // 2
        left = set(rucksack[0:halfway])
        right = set(rucksack[halfway:])
        common_item = list(set.intersection(left, right))[0] #extract letter
        priority_sum += priority(common_item)
    return priority_sum

def part2():
    badge_sum = 0
    GROUP_SIZE = 3
    curr_group = []
    for i, elf in enumerate(input):
        if i % GROUP_SIZE == 0 and i != 0:
            badge_sum += priority(badge(curr_group))
            curr_group = []
        curr_group.append(elf)
    return badge_sum

def badge(group):
    knapsacks = [set(elf) for elf in group]
    return list(set.intersection(*knapsacks))[0] #extract common letter

print(f"Answer for part 1: {part1()}")
print(f"Answer for part 2: {part2()}")