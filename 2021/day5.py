from aocd import get_data
#set session token first - https://github.com/wimglenn/advent-of-code-wim/issues/1
import numpy as np
import re

#Problem statement: https://adventofcode.com/2021/day/5

input = get_data(day=5, year=2021).split('\n')
input = [re.split(r',| -> ', i) for i in input]
input = [[int(i) for i in lst] for lst in input]

def make_seafloor(input):
    '''Create an array representing an ocean floor with hydrothermal vents'''
    max_x = max([max(i[0], i[2]) for i in input]) + 2
    max_y = max([max(i[1], i[3]) for i in input]) + 2
    return np.zeros([max_y, max_x])

def run(input, part1=True):
    seafloor = make_seafloor(input)

    for entry in input:
        x1, y1, x2, y2 = entry
        if part1 and not (x1 == x2 or y1 == y2):
            continue

        x_inc = -1 if x1 > x2 else 1 
        y_inc = -1 if y1 > y2 else 1
        if y1 == y2: #horizontal
            points = [(x1 + x_inc * i, y1) for i in range(abs(x2 - x1) + 1)]
        elif x1 == x2: #vertical
            points = [(x1, y1 + y_inc * i) for i in range(abs(y2 - y1) + 1)]
        else: #diagonal
            points = [(x1 + x_inc * i, y1 + y_inc * i) for i in range(abs(y2 - y1) + 1)]

        for point in points:
            seafloor[point[0]][point[1]] += 1

    return np.count_nonzero(seafloor >= 2)


if __name__ == '__main__':
    print(f"Part 1 solution: {run(input)}")
    print(f"Part 2 solution: {run(input, part1=False)}")
