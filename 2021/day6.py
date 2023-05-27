from aocd import get_data
#set session token first - https://github.com/wimglenn/advent-of-code-wim/issues/1
import numpy as np
import re

#Problem statement: https://adventofcode.com/2021/day/6

input = [int(i) for i in get_data(day=6, year=2021).split(',')]

def lanternfish_pop(input, n):
    '''Calculate how many lanternfish there will be in n (int) days, where today 
    is day 0.'''
    NEW_FISH_DAY = 8
    #bin the fish by their timer values
    fish = [input.count(i) for i in range(NEW_FISH_DAY + 1)]

    RESET_DAY = 6
    for day in range(n):
        current_zeros = fish.pop(0)
        fish[RESET_DAY] += current_zeros
        fish.append(current_zeros)
    return sum(fish)

if __name__ == '__main__':
    print(f"Part 1 solution: {lanternfish_pop(input, 80)}")
    print(f"Part 2 solution: {lanternfish_pop(input, 256)}")