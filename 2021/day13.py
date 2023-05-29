from aocd import get_data
#set session token first - https://github.com/wimglenn/advent-of-code-wim/issues/1
import numpy as np
import re

#Problem statement: https://adventofcode.com/2021/day/13

input = [i.split(',') for i in get_data(day=13, year=2021).split('\n') if i]
dots = [tuple(int(i) for i in line) for line in input if len(line) == 2]

AXIS_START = 11
folds = [re.split('=', line[0][AXIS_START:]) for line in input if len(line) == 1 and line[0]]
for i, fold in enumerate(folds):
    fold[1] = int(fold[1])

def fold_in(tuples, instruction):
    axis, line_num = instruction
    folded_tuples = []
    for tuple in tuples:
        this_x, this_y = tuple
        if axis == 'x' and this_x > line_num:
            this_x = line_num - abs(this_x - line_num)
        elif axis == 'y' and this_y > line_num:
            this_y = line_num - abs(this_y - line_num)
        folded_tuples.append((this_x, this_y))
    return list(set(folded_tuples))

def run(dots):
    for i, fold in enumerate(folds):
        dots = fold_in(dots, fold)
        if i == 0:
            print(f"Part 1 answer: {len(dots)}")

    array_x = max([dot[0] for dot in dots]) + 1
    array_y = max([dot[1] for dot in dots]) + 1
    message = np.ones((array_y, array_x), dtype=object)
    for dot in dots:
        x, y = dot
        message[y][x] = 0
    return message

np.set_printoptions(edgeitems=50, linewidth=1000)
print(run(dots))